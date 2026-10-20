"""BFF + static server for the DABS dashboard demo, live only.

Runs on the Python standard library, no pip install. Two jobs:

1. ``/api/patient/<bsn>`` - fetches the four federation endpoints, normalizes the
   200/503 responses into a model the frontend can draw, and keeps the API keys
   server-side.
2. Everything else - serves ``web/``.

Every request goes to the live federation API: there is no dataset and no fallback. When
that API is unreachable the response carries a single synthetic failure, so the UI shows
its empty-nodes banner and per-node strip instead of a stack trace.

Starting:
    python3 server.py
"""

import argparse
import json
import os
import pathlib
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path(__file__).resolve().parent
WEB = ROOT / "web"

ENDPOINTS = ["Patient", "Bloeddruk", "Lichaamsgewicht", "LichaamsLengte"]

# The nodes the federation is supposed to have. The flat live list simply leaves out nodes
# that dropped away. Without this list, offline/consent nodes vanish silently from the
# strip instead of appearing as "no data". Adjust with DABS_NODES.
KNOWN_NODES = [n.strip().lower() for n in
               os.environ.get("DABS_NODES", "zio,mumc,envida,vitala").split(",") if n.strip()]

# A node's federation API queries its own EHRbase and fans out to the other nodes.
# Querying one node is therefore enough. key1 belongs to MUMC; ZIO rejects it with a 401.
# These three differ per workstation. They can be set with a flag or an environment
# variable, so the code can stay unchanged on every machine.
# The demo runs at ZIO, so we query ZIO's federation API. That determines the perspective:
# the own node is queried without the informed-consent filter, all other nodes with it.
# Point this at another node and the picture changes accordingly.
FEDERATION_BASE = os.environ.get("DABS_FEDERATION_BASE", "http://federation.zio.local.dh.unimaas.nl")
KEY_NORMAL = os.environ.get("DABS_KEY", "key2")
KEY_BTG = os.environ.get("DABS_BTG_KEY", "btgkey2")


def own_node_from_url(base: str) -> str:
    """Derives the own node from 'federation.<node>.local.dh.unimaas.nl'."""
    host = urllib.parse.urlparse(base).hostname or ""
    parts = host.split(".")
    return parts[1] if len(parts) > 1 and parts[0] == "federation" else ""


CONFIG = {
    "timeout": 30,
    "federation_base": FEDERATION_BASE,
    "key": KEY_NORMAL,
    "btg_key": KEY_BTG,
    "eigen_node": own_node_from_url(FEDERATION_BASE),
}


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------
# The federation API returns a flat list per endpoint, with a ``Provider`` per record that
# names the node and all fields in PascalCase. The rest of this server and the frontend
# work on the old shape: a list per node with snake_case fields. These functions translate
# one into the other, so only fetch_live needs to know that the format has changed.
def _snake(name: str) -> str:
    """PascalCase -> snake_case. 'LengteDatumTijd' -> 'lengte_datum_tijd'."""
    out = []
    for i, char in enumerate(name):
        prev = name[i - 1] if i else ""
        if (char.isupper() and i and prev != "_"
                and (not prev.isupper()
                     or (i + 1 < len(name) and name[i + 1].islower()))):
            out.append("_")
        out.append(char.lower())
    return "".join(out)


def _find(node: dict, name: str, default=None):
    """Case-insensitively pull one key from a dict."""
    for key, value in node.items():
        if key.lower() == name.lower():
            return value
    return default


def _convert(node):
    """Converts a live value to snake_case.

    Two nested conventions are unwrapped in the process: ``{Magnitude, Units}`` (a
    measurement) becomes ``{"magnitude": ..., "units": ...}`` and ``{Value, Code,
    Terminology}`` (a coded value) becomes its ``Value``.
    """
    if isinstance(node, dict):
        keys = {key.lower() for key in node}
        if keys == {"magnitude", "units"}:
            return {"magnitude": _find(node, "Magnitude"), "units": _find(node, "Units")}
        if keys <= {"value", "code", "terminology"}:
            return _find(node, "Value")
        return {_snake(key): _convert(value) for key, value in node.items()}
    if isinstance(node, list):
        return [_convert(item) for item in node]
    return node


def _unfold(record: dict, source: str, magnitude: str, units: str) -> None:
    """``GewichtWaarde: {Magnitude, Units}`` -> separate ``..._magnitude`` and ``..._units``."""
    value = record.pop(source, None)
    if isinstance(value, dict):
        record[magnitude] = value.get("magnitude")
        record[units] = value.get("units")


def _norm_weight(record: dict) -> dict:
    _unfold(record, "gewicht_waarde", "gewichtwaarde_magnitude", "gewichtwaarde_units")
    return record


def _norm_length(record: dict) -> dict:
    _unfold(record, "lengte_waarde", "lengtewaarde_magnitude", "lengtewaarde_units")
    return record


def _norm_blood_pressure(record: dict) -> dict:
    # Unlike weight and length, the key here carries no "Value": the frontend reads
    # ``systolische_bloeddruk`` as a number, not as an object.
    for field in ("systolische_bloeddruk", "diastolische_bloeddruk", "gemiddelde_bloeddruk"):
        _unfold(record, field, field, f"{field}_units")
    # AnatomischeLocatie can be a coded value or a {Locatie, Lateraliteit} object;
    # the frontend reads ``locatie``.
    if isinstance(record.get("anatomische_locatie"), str):
        record["anatomische_locatie"] = {"locatie": record["anatomische_locatie"], "lateraliteit": None}
    return record


def _norm_patient(record: dict) -> dict:
    # The frontend reads this as a bool; the API sends a coded value that is always truthy,
    # and then "Ja" would always appear on screen.
    record["overlijdens_indicator"] = str(record.get("overlijdens_indicator") or "").strip().lower() in {
        "dead", "ja", "true"}
    return record


NORMALIZERS = {
    "Patient": _norm_patient,
    "Bloeddruk": _norm_blood_pressure,
    "Lichaamsgewicht": _norm_weight,
    "LichaamsLengte": _norm_length,
}


def normalize_live(payload, endpoint: str) -> dict:
    """Converts the flat live list into the old shape per node.

    Groups by ``Provider`` into ``{"<node>_federation": [...]}`` with snake_case fields.
    A payload that already has the old successes/failures shape passes through unchanged.
    """
    if not isinstance(payload, list):
        return payload
    per_node = {}
    for record in payload:
        node = str(record.get("Provider") or "onbekend").lower()
        converted = NORMALIZERS.get(endpoint, lambda r: r)(_convert(record))
        per_node.setdefault(f"{node}_federation", []).append(converted)
    return per_node


def fetch_live(endpoint: str, bsn: str, requester: str, btg: bool) -> dict:
    """Fetches one endpoint from the federation API.

    A 503 is not an error here: as long as not all nodes are healthy that is the normal
    answer, so we simply read the body. The flat live list is immediately normalized here
    into the old shape per node.
    """
    qs = urllib.parse.urlencode({"bsn": bsn, "requester": requester})
    req = urllib.request.Request(
        f"{CONFIG['federation_base']}/{endpoint}?{qs}",
        headers={"X-API-Key": CONFIG["btg_key"] if btg else CONFIG["key"],
                 "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=CONFIG["timeout"]) as resp:
            return normalize_live(json.loads(resp.read()), endpoint)
    except urllib.error.HTTPError as err:
        if err.code == 503:
            return normalize_live(json.loads(err.read()), endpoint)
        raise


def get_payload(endpoint: str, bsn: str, requester: str, btg: bool) -> dict:
    """Fetches one live endpoint, collapsing a transport failure into a synthetic payload.

    When the federation API itself is unreachable we know nothing per node. Showing that
    as one clear message is more honest than guessing per node.
    """
    try:
        return fetch_live(endpoint, bsn, requester, btg)
    except Exception as err:
        return {"successes": {}, "failures": {"federatie_federation": {
            "error": type(err).__name__,
            "message": f"{err} — {CONFIG['federation_base']}/{endpoint}"}}}


# ---------------------------------------------------------------------------
# Normalizing
# ---------------------------------------------------------------------------
def split_payload(payload: dict) -> tuple:
    """Pulls (per_node_records, failures) out of a 200 or 503 body."""
    if "successes" in payload or "failures" in payload:
        return payload.get("successes", {}), payload.get("failures", {})
    return payload, {}


def node_label(key: str) -> str:
    return key.removesuffix("_federation")


def flatten(per_node: dict, date_field: str) -> list:
    """Flattens the per-node lists into one series, enriched with _source and sorted by date."""
    rows = []
    for node_key, records in per_node.items():
        for record in records:
            row = dict(record)
            row["_source"] = node_label(node_key)
            rows.append(row)
    rows.sort(key=lambda r: r.get(date_field) or "")
    return rows


def build_response(bsn: str, requester: str, btg: bool) -> dict:
    start = time.time()

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = dict(
            zip(
                ENDPOINTS,
                pool.map(lambda ep: get_payload(ep, bsn, requester, btg), ENDPOINTS),
            )
        )

    per_endpoint, all_failures, all_nodes = {}, {}, set()
    for endpoint, payload in results.items():
        successes, failures = split_payload(payload)
        per_endpoint[endpoint] = successes
        all_failures.update(failures)
        all_nodes.update(node_label(k) for k in successes)
        all_nodes.update(node_label(k) for k in failures)

    # The live API leaves out nodes that dropped away; fill in the expected set so an
    # offline or consent-blocked node appears as such in the strip.
    all_nodes.update(KNOWN_NODES)

    def series_for(endpoint, field):
        return flatten(per_endpoint.get(endpoint, {}), field)

    blood_pressure = series_for("Bloeddruk", "bloeddruk_datum_tijd")
    weight = series_for("Lichaamsgewicht", "gewicht_datum_tijd")
    length = series_for("LichaamsLengte", "lengte_datum_tijd")
    patient = series_for("Patient", "start_time")

    # Determine per node what is going on. Three outcomes the UI shows separately:
    # offline (node did not answer), consent_blocked (node answered, but the
    # informed-consent filter let nothing through) and ok.
    counts = {}
    for series in (blood_pressure, weight, length, patient):
        for row in series:
            counts[row["_source"]] = counts.get(row["_source"], 0) + 1

    # The API does not say why a node returns zero records. Two cases can be
    # distinguished: if no single node delivers anything, the patient is not there; if
    # another node does and break-the-glass is off, then the consent filter is the reason.
    someone_has_data = any(counts.values())
    own_node = CONFIG["eigen_node"]

    nodes = []
    # Own node first: it determines the perspective and is not consent-filtered.
    for name in sorted(all_nodes, key=lambda n: (n != own_node, n)):
        count = counts.get(name, 0)
        base = {"name": name, "own": name == own_node}
        if f"{name}_federation" in all_failures:
            error = all_failures[f"{name}_federation"]
            message = error.get("message") if isinstance(error, dict) else str(error)
            nodes.append({**base, "status": "offline", "records": 0, "message": message})
        elif count:
            nodes.append({**base, "status": "ok", "records": count, "message": None})
        elif someone_has_data and not btg:
            nodes.append({**base, "status": "consent_blocked", "records": 0,
                          "message": "Geen toestemming voor gegevensuitwisseling"})
        else:
            nodes.append({**base, "status": "geen_data", "records": 0,
                          "message": "Geen gegevens voor dit BSN"})

    result = {
        "bsn": bsn,
        "nodes": nodes,
        "patient": patient,
        "bloeddruk": blood_pressure,
        "gewicht": weight,
        "lengte": length,
        "meta": {
            "btg": btg,
            "requester": requester,
            "duration_ms": int((time.time() - start) * 1000),
            "mode": "nodes",
            "dataset": None,
            "eigen_node": CONFIG["eigen_node"],
            "btg_extra_records": None,
            "sources": ["live"],
        },
    }

    return result


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
MIME = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8", ".json": "application/json",
        ".svg": "image/svg+xml", ".ico": "image/x-icon"}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} - {fmt % args}")

    def _send(self, body: bytes, content_type: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data, status: int = 200):
        self._send(json.dumps(data, ensure_ascii=False).encode(), "application/json", status)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path.startswith("/api/patient/"):
            bsn = path.rsplit("/", 1)[-1]
            if not bsn.isdigit():
                return self._json({"error": "Ongeldig BSN"}, 400)
            requester = query.get("requester", ["Rolf"])[0]
            btg = query.get("btg", ["false"])[0].lower() == "true"
            try:
                return self._json(build_response(bsn, requester, btg))
            except Exception as err:  # never let a demo crash on a stack trace
                return self._json({"error": f"{type(err).__name__}: {err}"}, 500)

        if path == "/api/config":
            return self._json({"mode": "live", "dataset": None})

        file = WEB / "index.html" if path in ("/", "") else WEB / path.lstrip("/")
        try:
            file = file.resolve()
            file.relative_to(WEB.resolve())  # blocks path traversal
            data = file.read_bytes()
        except (OSError, ValueError):
            return self._send(b"Niet gevonden", "text/plain; charset=utf-8", 404)
        self._send(data, MIME.get(file.suffix, "application/octet-stream"))


def main():
    parser = argparse.ArgumentParser(description="DABS dashboard demo (live)")
    parser.add_argument("--port", type=int, default=8800)
    parser.add_argument("--timeout", type=int, default=30,
                        help="seconden per federation-call voordat deze afbreekt")
    parser.add_argument("--federation-base", default=FEDERATION_BASE,
                        help="basis-URL van de federation API van je eigen node")
    parser.add_argument("--key", default=KEY_NORMAL, help="X-API-Key van je node")
    parser.add_argument("--btg-key", default=KEY_BTG, help="break-the-glass key van je node")
    parser.add_argument("--host", default="0.0.0.0",
                        help="luisteradres; 0.0.0.0 om de demo op het netwerk te delen")
    parser.add_argument("--eigen-node", default=None,
                        help="naam van de eigen node; standaard afgeleid uit de federation-URL")
    args = parser.parse_args()

    CONFIG["timeout"] = args.timeout
    CONFIG["federation_base"] = args.federation_base.rstrip("/")
    CONFIG["key"] = args.key
    CONFIG["btg_key"] = args.btg_key
    CONFIG["eigen_node"] = args.eigen_node or own_node_from_url(CONFIG["federation_base"])

    print("\n  DABS demo   live · alleen nodes")
    print(f"  federation  {CONFIG['federation_base']}  (eigen node: {CONFIG['eigen_node'] or 'onbekend'})")
    print(f"  open        http://localhost:{args.port}\n")

    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
