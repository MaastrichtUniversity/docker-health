"""A tiny stdlib HTTP server that emulates the live federation API for tests.

Seeded from ``tests/samples/`` (flat list, ``200`` by default). A test can retarget any
endpoint to another status/shape, or point the application at a closed port to exercise
connection-refused. No test ever needs the real network.

Usage::

    mock = MockFederation()
    mock.start()                      # binds 127.0.0.1 on an ephemeral port
    server_info = mock.base_url       # http://127.0.0.1:<port>
    ...
    mock.stop()
"""

import json
import pathlib
import socket
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import samples

DEFAULT_STATUS = 200


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # keep the test output clean
        pass

    def do_GET(self):  # noqa: N802 (BaseHTTPRequestHandler API)
        mock = self.server.mock
        parsed = urllib.parse.urlparse(self.path)
        endpoint = parsed.path.strip("/")

        mock.requests.append({
            "path": self.path,
            "endpoint": endpoint,
            "headers": {k.lower(): v for k, v in self.headers.items()},
            "api_key": self.headers.get("X-API-Key"),
        })

        spec = mock.responses.get(endpoint)
        if spec is None:
            return self._send(404, {"error": f"onbekend endpoint: {endpoint}"})

        return self._send(spec["status"], spec["body"])

    def _send(self, status, body):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


class MockFederation:
    """Configurable in-process federation stand-in."""

    def __init__(self):
        self.samples = samples.load_all()
        self.requests = []
        self.responses = {}
        self._server = None
        self._thread = None
        self.reset()

    # -- configuration -----------------------------------------------------
    def reset(self):
        """Back to the default: flat-list 200 with the full samples."""
        self.requests = []
        self.responses = {
            endpoint: {"status": DEFAULT_STATUS, "body": list(self.samples[endpoint])}
            for endpoint in samples.ENDPOINTS
        }

    def set_flat(self, endpoint, records=None, status=DEFAULT_STATUS):
        """Serve a flat live list (the primary shape)."""
        body = records if records is not None else self.samples[endpoint]
        self.responses[endpoint] = {"status": status, "body": body}

    def set_raw(self, endpoint, body, status=DEFAULT_STATUS):
        """Serve an arbitrary JSON body, e.g. the legacy ``{successes, failures}`` shape."""
        self.responses[endpoint] = {"status": status, "body": body}

    def set_all(self, body, status=DEFAULT_STATUS):
        for endpoint in samples.ENDPOINTS:
            self.responses[endpoint] = {"status": status, "body": body}

    def set_samples(self, status):
        """Serve every endpoint's flat sample list with a non-200 status (503/401)."""
        for endpoint in samples.ENDPOINTS:
            self.responses[endpoint] = {"status": status, "body": list(self.samples[endpoint])}

    # -- lifecycle ---------------------------------------------------------
    def start(self):
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self._server.mock = self
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self.base_url

    @property
    def base_url(self) -> str:
        host, port = self._server.server_address[:2]
        return f"http://{host}:{port}"

    def stop(self):
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None


def free_port() -> int:
    """Return a currently-unused localhost port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def refused_base_url() -> str:
    """Return a base URL on a closed port, to trigger connection-refused."""
    return f"http://127.0.0.1:{free_port()}"
