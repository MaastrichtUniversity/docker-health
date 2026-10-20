"""Integration tests: the real ``server.py`` HTTP app against a mock federation.

The mock federation server (``support/mock_federation.py``) is seeded from
``tests/samples/``. The application is spawned as a subprocess with
``--federation-base`` pointing at the mock, on an ephemeral port. No test touches the
real federation API.
"""

import builtins
import contextlib
import json
import pathlib
import subprocess
import sys
import time
import unittest
import urllib.error
import urllib.request
from unittest import mock as unittest_mock

from support import samples
from support.mock_federation import MockFederation, free_port, refused_base_url
from support.server_loader import PROJECT_ROOT, SERVER_PATH, load_server

server = load_server()


def http_get(url):
    """GET a URL and return (status, parsed json); 4xx/5xx bodies are parsed too."""
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as err:
        raw = err.read()
        try:
            return err.code, json.loads(raw)
        except ValueError:
            return err.code, raw


@contextlib.contextmanager
def running_app(federation_base, key="testkey", btg_key="testbtg", eigen_node="zio"):
    """Spawn ``server.py`` on an ephemeral port; yield its base URL."""
    port = free_port()
    proc = subprocess.Popen(
        [
            sys.executable, str(SERVER_PATH),
            "--host", "127.0.0.1",
            "--port", str(port),
            "--federation-base", federation_base,
            "--key", key,
            "--btg-key", btg_key,
            "--eigen-node", eigen_node,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=str(PROJECT_ROOT),
    )
    base = f"http://127.0.0.1:{port}"
    try:
        _wait_until_up(base + "/api/config", proc)
        yield base
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


def _wait_until_up(url, proc, attempts=100, delay=0.05):
    for _ in range(attempts):
        if proc.poll() is not None:
            raise AssertionError(f"server.py exited early with code {proc.returncode}")
        try:
            with urllib.request.urlopen(url, timeout=0.5) as resp:
                if resp.status == 200:
                    return
        except (urllib.error.URLError, OSError):
            time.sleep(delay)
    raise AssertionError(f"server did not come up on {url}")


class LiveEndToEndTest(unittest.TestCase):
    """Drives the full HTTP path: browser-style request -> server.py -> mock federation."""

    @classmethod
    def setUpClass(cls):
        cls.mock = MockFederation()
        cls.mock.start()
        cls._app = running_app(cls.mock.base_url)
        cls.app_base = cls._app.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls._app.__exit__(None, None, None)
        cls.mock.stop()

    def setUp(self):
        self.mock.reset()

    def patient_url(self, btg=False):
        return f"{self.app_base}/api/patient/999990603?requester=Rolf&btg={'true' if btg else 'false'}"

    def nodes_by_name(self, result):
        return {node["name"]: node for node in result["nodes"]}

    # -- shapes ------------------------------------------------------------
    def test_new_shape_200_returns_four_nodes_with_sample_counts(self):
        status, result = http_get(self.patient_url())
        self.assertEqual(status, 200)

        self.assertEqual(len(result["patient"]), samples.EXPECTED_COUNTS["Patient"])
        self.assertEqual(len(result["bloeddruk"]), samples.EXPECTED_COUNTS["Bloeddruk"])
        self.assertEqual(len(result["gewicht"]), samples.EXPECTED_COUNTS["Lichaamsgewicht"])
        self.assertEqual(len(result["lengte"]), samples.EXPECTED_COUNTS["LichaamsLengte"])

        nodes = self.nodes_by_name(result)
        self.assertEqual(set(nodes), set(samples.KNOWN_NODES))
        for name in samples.KNOWN_NODES:
            self.assertEqual(nodes[name]["status"], "ok", name)
            # 1 patient + 6 bloeddruk + 6 gewicht + 1 lengte
            self.assertEqual(nodes[name]["records"], 14, name)

    def test_new_shape_own_node_first(self):
        _, result = http_get(self.patient_url())
        self.assertEqual(result["nodes"][0]["name"], "zio")
        self.assertTrue(result["nodes"][0]["own"])

    def test_new_shape_meta_is_live_only(self):
        _, result = http_get(self.patient_url())
        meta = result["meta"]
        self.assertEqual(meta["mode"], "nodes")
        self.assertIsNone(meta["dataset"])
        self.assertIsNone(meta["btg_extra_records"])
        self.assertEqual(meta["sources"], ["live"])

    def test_length_series_sorted_by_lengte_datum_tijd(self):
        _, result = http_get(self.patient_url())
        dates = [row["lengte_datum_tijd"] for row in result["lengte"]]
        self.assertEqual(dates, sorted(dates))
        zio = next(row for row in result["lengte"] if row["_source"] == "zio")
        self.assertEqual(zio["start_time"], "2001-03-19T11:43:13.174")
        self.assertEqual(zio["lengte_datum_tijd"], "2001-03-19T10:43:13.174")

    def test_old_shape_200(self):
        for endpoint in samples.ENDPOINTS:
            per_node = server.normalize_live(samples.load(endpoint), endpoint)
            self.mock.set_raw(endpoint, {"successes": per_node, "failures": {}})

        status, result = http_get(self.patient_url())
        self.assertEqual(status, 200)
        nodes = self.nodes_by_name(result)
        for name in samples.KNOWN_NODES:
            self.assertEqual(nodes[name]["status"], "ok", name)
        self.assertEqual(len(result["bloeddruk"]), 24)
        self.assertEqual(len(result["gewicht"]), 24)

    def test_503_is_read_as_data(self):
        self.mock.set_samples(503)
        status, result = http_get(self.patient_url())
        self.assertEqual(status, 200)
        nodes = self.nodes_by_name(result)
        for name in samples.KNOWN_NODES:
            self.assertEqual(nodes[name]["status"], "ok", name)
        self.assertEqual(len(result["bloeddruk"]), 24)
        self.assertEqual(len(result["gewicht"]), 24)

    def test_401_collapses_to_offline_federation(self):
        self.mock.set_samples(401)
        status, result = http_get(self.patient_url())
        self.assertEqual(status, 200)
        nodes = self.nodes_by_name(result)
        # The 401 is caught and collapsed into one synthetic federation failure.
        self.assertIn("federatie", nodes)
        self.assertEqual(nodes["federatie"]["status"], "offline")
        for name in samples.KNOWN_NODES:
            self.assertEqual(nodes[name]["status"], "geen_data", name)

    def test_federation_key_selected_by_btg_toggle(self):
        self.mock.requests.clear()
        http_get(self.patient_url(btg=False))
        normal_keys = {r["api_key"] for r in self.mock.requests}
        self.assertEqual(normal_keys, {"testkey"})

        self.mock.requests.clear()
        http_get(self.patient_url(btg=True))
        btg_keys = {r["api_key"] for r in self.mock.requests}
        self.assertEqual(btg_keys, {"testbtg"})

    # -- config parity -----------------------------------------------------
    def test_api_config_returns_live(self):
        status, body = http_get(f"{self.app_base}/api/config")
        self.assertEqual(status, 200)
        self.assertEqual(body["mode"], "live")
        self.assertIsNone(body["dataset"])

    def test_invalid_bsn_returns_400(self):
        status, body = http_get(f"{self.app_base}/api/patient/abc?requester=Rolf")
        self.assertEqual(status, 400)
        self.assertIn("error", body)


class ConnectionRefusedTest(unittest.TestCase):
    def test_unreachable_federation_returns_offline_nodes(self):
        with running_app(refused_base_url()) as app_base:
            status, result = http_get(
                f"{app_base}/api/patient/999990603?requester=Rolf&btg=false"
            )
        self.assertEqual(status, 200)
        nodes = {node["name"]: node for node in result["nodes"]}
        self.assertEqual(nodes["federatie"]["status"], "offline")
        self.assertEqual(nodes["federatie"]["records"], 0)
        for name in samples.KNOWN_NODES:
            self.assertEqual(nodes[name]["status"], "geen_data", name)
        self.assertEqual(result["meta"]["mode"], "nodes")
        self.assertIsNone(result["meta"]["dataset"])


class NoProductFixturesTest(unittest.TestCase):
    """Guard: no product fixture directory may exist or be read."""

    def test_no_fixture_directory_in_product(self):
        for name in ("fixtures", "fixtures-rich"):
            self.assertFalse((PROJECT_ROOT / name).exists(), f"{name}/ must not exist")

    def test_server_module_has_no_fixture_api(self):
        for attr in ("load_fixture", "fixture_dir", "fixture_bsn", "fixture_total", "fixtures"):
            self.assertFalse(hasattr(server, attr), f"server.{attr} must not exist")

    def test_server_source_mentions_no_fixture(self):
        source = pathlib.Path(server.__file__).read_text(encoding="utf-8").lower()
        self.assertNotIn("fixture", source)

    def test_build_response_reads_no_fixture_files(self):
        real_open = builtins.open
        opened = []

        def guarded_open(file, *args, **kwargs):
            path = str(file)
            opened.append(path)
            if "fixture" in path.lower():
                raise AssertionError(f"a code path tried to read a fixture: {path}")
            return real_open(file, *args, **kwargs)

        with unittest_mock.patch.object(builtins, "open", guarded_open):
            with unittest_mock.patch.object(server, "get_payload", return_value={}):
                server.build_response("999990603", "Rolf", False)

        self.assertFalse(any("fixture" in path.lower() for path in opened))


if __name__ == "__main__":
    unittest.main()
