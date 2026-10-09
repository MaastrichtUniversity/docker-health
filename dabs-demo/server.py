"""BFF + statische server voor de DABS dashboard demo.

Draait op de Python standard library, zonder pip install. Twee taken:

1. ``/api/patient/<bsn>`` - haalt de vier federation-endpoints op, normaliseert de
   200/503-responses tot een model dat de frontend kan tekenen, en houdt de API-keys
   serverside.
2. Alles daarbuiten - serveert ``web/``.

Modi (``--mode``):
  fixture  De vastgelegde responses uit fixtures/. Standaard, want het cluster levert
           op dit moment geen data.
  live     De echte federation API. Valt per endpoint terug op de fixture als de node
           niet antwoordt, zodat een demo niet omvalt op een wegvallende node.

Starten:
    python3 server.py                      # fixtures, getrouwe set
    python3 server.py --dataset rich       # fixtures, verrijkte meetreeksen
    python3 server.py --mode live          # echte federation API
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

# De federation API van een node bevraagt zijn eigen EHRbase en fant uit naar de andere
# nodes. Een node bevragen volstaat dus. key1 hoort bij MUMC; ZIO wijst hem af met een 401.
# Deze drie verschillen per werkplek. Ze zijn in te stellen met een vlag of een
# omgevingsvariabele, zodat de code op elke machine ongewijzigd kan blijven.
# De demo draait bij ZIO, dus bevragen we de federation API van ZIO. Dat bepaalt het
# perspectief: de eigen node wordt zonder informed-consent-filter bevraagd, alle andere
# nodes mét. Wijs dit naar een andere node en het beeld verandert navenant.
FEDERATION_BASE = os.environ.get("DABS_FEDERATION_BASE", "http://federation.zio.local.dh.unimaas.nl")
KEY_NORMAAL = os.environ.get("DABS_KEY", "key2")
KEY_BTG = os.environ.get("DABS_BTG_KEY", "btgkey2")

def eigen_node_uit_url(base: str) -> str:
    """Leidt de eigen node af uit 'federation.<node>.local.dh.unimaas.nl'."""
    host = urllib.parse.urlparse(base).hostname or ""
    delen = host.split(".")
    return delen[1] if len(delen) > 1 and delen[0] == "federation" else ""


CONFIG = {
    "mode": "fixture",
    "dataset": "faithful",
    "timeout": 30,
    "federation_base": FEDERATION_BASE,
    "key": KEY_NORMAAL,
    "btg_key": KEY_BTG,
    "eigen_node": eigen_node_uit_url(FEDERATION_BASE),
}


# ---------------------------------------------------------------------------
# Ophalen
# ---------------------------------------------------------------------------
def fixture_dir(dataset: str) -> pathlib.Path:
    return ROOT / ("fixtures-rich" if dataset == "rich" else "fixtures")


def fixture_bsn(dataset: str) -> str:
    """Het BSN waar de fixtures over gaan, gelezen uit de Patient-fixture."""
    patient = json.loads((fixture_dir(dataset) / "Patient.btg.json").read_text())
    for records in patient.values():
        for record in records:
            nummers = record.get("identificatienummer") or []
            if nummers:
                return str(nummers[0])
    return ""


def load_fixture(endpoint: str, btg: bool, dataset: str, bsn: str = None) -> dict:
    print(f"load_fixture")
    naam = f"{endpoint}.btg.json" if btg else f"{endpoint}.json"
    payload = json.loads((fixture_dir(dataset) / naam).read_text())
    # De fixtures beschrijven één patiënt. Een ander BSN hoort leeg terug te komen,
    # anders toont de demo de gegevens van de demopatiënt onder een vreemd nummer.
    if bsn is not None and bsn != fixture_bsn(dataset):
        return {node: [] for node in payload}
    return payload


def fetch_live(endpoint: str, bsn: str, requester: str, btg: bool) -> dict:
    """Haalt een endpoint op bij de federation API.

    Een 503 is hier geen fout: zolang niet alle nodes gezond zijn is dat het normale
    antwoord, met de geslaagde nodes in ``successes``. Die body lezen we dus gewoon uit.
    """
    print(f"fetch_live")
    qs = urllib.parse.urlencode({"bsn": bsn, "requester": requester})
    req = urllib.request.Request(
        f"{CONFIG['federation_base']}/{endpoint}?{qs}",
        headers={"X-API-Key": CONFIG["btg_key"] if btg else CONFIG["key"],
                 "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=CONFIG["timeout"]) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as err:
        if err.code == 503:
            return json.loads(err.read())
        raise


def get_payload(endpoint: str, bsn: str, requester: str, btg: bool, dataset: str,
                alleen_nodes: bool = False) -> tuple:
    """Levert (payload, bron) waarbij bron 'live', 'fixture' of 'fixture-fallback' is.

    Met ``alleen_nodes`` wordt uitsluitend de echte federation API bevraagd en is er geen
    terugval op fixtures: wat de nodes leveren is wat je ziet, ook als dat niets is.
    """
    print(f"get_payload")
    if alleen_nodes:
        try:
            return fetch_live(endpoint, bsn, requester, btg), "live"
        except Exception as err:
            # De federation API zelf is onbereikbaar, dus we weten niets per node.
            # Dat als één duidelijke melding tonen is eerlijker dan per node gokken.
            return {"successes": {}, "failures": {"federatie_federation": {
                "error": type(err).__name__,
                "message": f"{err} — {CONFIG['federation_base']}/{endpoint}"}}}, "live"

    if CONFIG["mode"] != "live":
        print(f"get_payload load_fixture")
        return load_fixture(endpoint, btg, dataset, bsn), "fixture"
    try:
        payload = fetch_live(endpoint, bsn, requester, btg)
        # Een response zonder enige geslaagde node is voor een demo waardeloos; val terug.
        successes = payload.get("successes", payload)
        if not any(successes.get(k) for k in successes):
            if not payload.get("failures"):
                return payload, "live"
            print(f"get_payload failures load_fixture")
            return load_fixture(endpoint, btg, dataset, bsn), "fixture-fallback"
        return payload, "live"
    except Exception as ex:
        print(f"error: {ex}")
        print(f"get_payload Exception load_fixture")
        return load_fixture(endpoint, btg, dataset, bsn), "fixture-fallback"


# ---------------------------------------------------------------------------
# Normaliseren
# ---------------------------------------------------------------------------
def split_payload(payload: dict) -> tuple:
    """Haalt (per_node_records, failures) uit een 200- of 503-body."""
    if "successes" in payload or "failures" in payload:
        return payload.get("successes", {}), payload.get("failures", {})
    return payload, {}


def node_label(key: str) -> str:
    return key.removesuffix("_federation")


def flatten(per_node: dict, datum_veld: str) -> list:
    """Plat de per-node lijsten tot een reeks, verrijkt met _source en gesorteerd op datum."""
    rijen = []
    for node_key, records in per_node.items():
        for record in records:
            rij = dict(record)
            rij["_source"] = node_label(node_key)
            rijen.append(rij)
    rijen.sort(key=lambda r: r.get(datum_veld) or "")
    return rijen


def fixture_totaal(bsn: str, dataset: str, btg: bool) -> int:
    """Telt alle records in een fixtureset, om te bepalen wat break-the-glass oplevert."""
    print(f"fixture_totaal")
    return sum(
        len(records)
        for endpoint in ENDPOINTS
        for records in load_fixture(endpoint, btg, dataset, bsn).values()
    )


def bepaal_modus(bronnen: set) -> str:
    """Vertaalt de gebruikte databronnen naar een label voor de statusstrip."""
    if bronnen == {"live"}:
        return "live"
    if bronnen == {"fixture"}:
        return "fixture"
    if bronnen == {"fixture-fallback"}:
        return "fallback"  # live geprobeerd, geen enkele node leverde
    return "gemengd"


def build_response(bsn: str, requester: str, btg: bool, dataset: str,
                   alleen_nodes: bool = False) -> dict:
    start = time.time()

    with ThreadPoolExecutor(max_workers=4) as pool:
        resultaten = dict(
            zip(
                ENDPOINTS,
                pool.map(lambda ep: get_payload(ep, bsn, requester, btg, dataset, alleen_nodes), ENDPOINTS),
            )
        )

    per_endpoint, bronnen = {}, set()
    alle_failures, alle_nodes = {}, set()
    for endpoint, (payload, bron) in resultaten.items():
        successes, failures = split_payload(payload)
        per_endpoint[endpoint] = successes
        alle_failures.update(failures)
        alle_nodes.update(node_label(k) for k in successes)
        alle_nodes.update(node_label(k) for k in failures)
        bronnen.add(bron)

    def voor(endpoint, veld):
        return flatten(per_endpoint.get(endpoint, {}), veld)

    bloeddruk = voor("Bloeddruk", "bloeddruk_datum_tijd")
    gewicht = voor("Lichaamsgewicht", "gewicht_datum_tijd")
    lengte = voor("LichaamsLengte", "lengte_datum_tijd")
    patient = voor("Patient", "start_time")

    # Per node bepalen wat er aan de hand is. Drie uitkomsten die de UI los toont:
    # offline (node antwoordde niet), consent_blocked (node antwoordde, maar het
    # informed-consent-filter liet niets door) en ok.
    tellingen = {}
    for reeks in (bloeddruk, gewicht, lengte, patient):
        for rij in reeks:
            tellingen[rij["_source"]] = tellingen.get(rij["_source"], 0) + 1

    # De API vertelt niet waarom een node nul records teruggeeft. Twee gevallen zijn wel
    # te onderscheiden: levert geen enkele node iets, dan is de patiënt er niet; levert
    # een andere node wel en staat break-the-glass uit, dan is het consent-filter de reden.
    iemand_heeft_data = any(tellingen.values())
    eigen = CONFIG["eigen_node"]

    nodes = []
    # Eigen node eerst: die bepaalt het perspectief en wordt niet consent-gefilterd.
    for naam in sorted(alle_nodes, key=lambda n: (n != eigen, n)):
        aantal = tellingen.get(naam, 0)
        basis = {"name": naam, "own": naam == eigen}
        if f"{naam}_federation" in alle_failures:
            fout = alle_failures[f"{naam}_federation"]
            bericht = fout.get("message") if isinstance(fout, dict) else str(fout)
            nodes.append({**basis, "status": "offline", "records": 0, "message": bericht})
        elif aantal:
            nodes.append({**basis, "status": "ok", "records": aantal, "message": None})
        elif iemand_heeft_data and not btg:
            nodes.append({**basis, "status": "consent_blocked", "records": 0,
                          "message": "Geen toestemming voor gegevensuitwisseling"})
        else:
            nodes.append({**basis, "status": "geen_data", "records": 0,
                          "message": "Geen gegevens voor dit BSN"})


    print(f"check mode {CONFIG["mode"]}")
    # Hoeveel records levert break-the-glass werkelijk op? Uit de fixtures exact te
    # bepalen; live zouden we daarvoor alles dubbel moeten ophalen, dus dan laten we het
    # open en houdt de UI het bij een algemene formulering.
    btg_extra = None
    if btg and not alleen_nodes and CONFIG["mode"] != "live":
        print(f"btg_extra")
        btg_extra = fixture_totaal(bsn, dataset, True) - fixture_totaal(bsn, dataset, False)

    result = {
        "bsn": bsn,
        "nodes": nodes,
        "patient": patient,
        "bloeddruk": bloeddruk,
        "gewicht": gewicht,
        "lengte": lengte,
        "meta": {
            "btg": btg,
            "requester": requester,
            "duration_ms": int((time.time() - start) * 1000),
            "mode": "nodes" if alleen_nodes else bepaal_modus(bronnen),
            "dataset": None if alleen_nodes else dataset,
            "eigen_node": CONFIG["eigen_node"],
            "btg_extra_records": btg_extra,
            "sources": sorted(bronnen),
        },
    }

    print(f"result: {result}")

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
        pad = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        print(CONFIG)

        if pad.startswith("/api/patient/"):
            bsn = pad.rsplit("/", 1)[-1]
            if not bsn.isdigit():
                return self._json({"error": "Ongeldig BSN"}, 400)
            requester = query.get("requester", ["Rolf"])[0]
            btg = query.get("btg", ["false"])[0].lower() == "true"
            # De client mag de dataset per verzoek kiezen; dat voedt de schakelaar
            # "alleen brondata", die de aangevulde reeksen buiten beeld houdt.
            dataset = query.get("dataset", [CONFIG["dataset"]])[0]
            if dataset not in ("faithful", "rich"):
                dataset = CONFIG["dataset"]
            # bron=nodes: uitsluitend de echte endpoints, geen fixtures, geen terugval.
            alleen_nodes = query.get("bron", ["demo"])[0] == "nodes"
            try:
                print(f"patient")
                return self._json(build_response(bsn, requester, btg, dataset, alleen_nodes))
            except Exception as err:  # nooit een demo laten klappen op een stacktrace
                print(f"patient")
                return self._json({"error": f"{type(err).__name__}: {err}"}, 500)

        if pad == "/api/config":
            return self._json({"mode": CONFIG["mode"], "dataset": CONFIG["dataset"]})

        bestand = WEB / "index.html" if pad in ("/", "") else WEB / pad.lstrip("/")
        try:
            bestand = bestand.resolve()
            bestand.relative_to(WEB.resolve())  # weert padtraversal
            data = bestand.read_bytes()
        except (OSError, ValueError):
            return self._send(b"Niet gevonden", "text/plain; charset=utf-8", 404)
        self._send(data, MIME.get(bestand.suffix, "application/octet-stream"))


def main():
    parser = argparse.ArgumentParser(description="DABS dashboard demo")
    parser.add_argument("--mode", choices=["fixture", "live"], default="fixture")
    parser.add_argument("--dataset", choices=["faithful", "rich"], default="faithful",
                        help="faithful = exact de brondata; rich = langere meetreeksen voor de grafieken")
    parser.add_argument("--port", type=int, default=8800)
    parser.add_argument("--timeout", type=int, default=30,
                        help="seconden per federation-call voordat op de fixture wordt teruggevallen")
    parser.add_argument("--federation-base", default=FEDERATION_BASE,
                        help="basis-URL van de federation API van je eigen node")
    parser.add_argument("--key", default=KEY_NORMAAL, help="X-API-Key van je node")
    parser.add_argument("--btg-key", default=KEY_BTG, help="break-the-glass key van je node")
    parser.add_argument("--host", default="0.0.0.0",
                        help="luisteradres; 0.0.0.0 om de demo op het netwerk te delen")
    parser.add_argument("--eigen-node", default=None,
                        help="naam van de eigen node; standaard afgeleid uit de federation-URL")
    args = parser.parse_args()

    CONFIG["mode"] = args.mode
    CONFIG["dataset"] = args.dataset
    CONFIG["timeout"] = args.timeout
    CONFIG["federation_base"] = args.federation_base.rstrip("/")
    CONFIG["key"] = args.key
    CONFIG["btg_key"] = args.btg_key
    CONFIG["eigen_node"] = args.eigen_node or eigen_node_uit_url(CONFIG["federation_base"])

    print(f"\n  DABS demo   mode={args.mode}  dataset={args.dataset}")
    print(f"  federation  {CONFIG['federation_base']}  (eigen node: {CONFIG['eigen_node'] or 'onbekend'})")
    if args.mode == "live":
        print("              (valt per endpoint terug op fixtures)")
    print(f"  open        http://localhost:{args.port}\n")

    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
