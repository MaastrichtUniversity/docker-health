"""Controleert of deze machine de DABS demo kan draaien.

Loopt van binnen naar buiten: eerst Python en de bestanden, dan de federation API, dan
de losse endpoints. Zo zie je meteen op welke laag het misgaat in plaats van alleen dat
er "niets werkt".

Draait op de standard library, net als de demo zelf.

Standaard wordt de federation API van ZIO bevraagd, want daar draait de demo. Dat bepaalt
het perspectief: de eigen node wordt zonder informed-consent-filter bevraagd, andere nodes
met. Wijs --federation-base naar een andere node en het beeld verandert navenant.

    python3 tools/check_omgeving.py
    python3 tools/check_omgeving.py --federation-base http://federation.mumc.local.dh.unimaas.nl
    python3 tools/check_omgeving.py --key key1 --btg-key btgkey1 --bsn 999990603
"""

import argparse
import json
import pathlib
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENDPOINTS = ["Patient", "Bloeddruk", "Lichaamsgewicht", "LichaamsLengte"]

GROEN, ROOD, GEEL, GRIJS, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[90m", "\033[0m"

resultaten = []


def meld(status: str, wat: str, detail: str = ""):
    """status: ok | fout | let op"""
    kleur = {"ok": GROEN, "fout": ROOD, "let op": GEEL}[status]
    teken = {"ok": "v", "fout": "x", "let op": "!"}[status]
    print(f"  {kleur}[{teken}]{RESET} {wat:<44} {GRIJS}{detail}{RESET}")
    resultaten.append(status)


def kop(tekst: str):
    print(f"\n{tekst}")
    print("  " + "-" * 72)


def haal(url: str, key: str = None, timeout: int = 20):
    """Levert (statuscode, body-of-tekst). Een HTTP-fout is hier data, geen exceptie."""
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    if key:
        req.add_header("X-API-Key", key)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read()
    except Exception as err:
        return None, f"{type(err).__name__}: {err}".encode()


# ---------------------------------------------------------------------------
# 1. De machine zelf
# ---------------------------------------------------------------------------
def check_machine(port: int):
    kop("1. Machine")

    versie = sys.version_info
    if versie >= (3, 9):
        meld("ok", "Python 3.9 of nieuwer", f"{versie.major}.{versie.minor}.{versie.micro}")
    else:
        meld("fout", "Python te oud (3.9+ nodig)", f"{versie.major}.{versie.minor}")

    ontbreekt = [p for p in ["server.py", "web/index.html", "web/app.js", "web/styles.css"]
                 if not (ROOT / p).exists()]
    if ontbreekt:
        meld("fout", "Demobestanden compleet", f"ontbreekt: {', '.join(ontbreekt)}")
    else:
        meld("ok", "Demobestanden compleet", "server.py + web/")

    for naam in ("fixtures", "fixtures-rich"):
        bestanden = sorted((ROOT / naam).glob("*.json")) if (ROOT / naam).is_dir() else []
        if len(bestanden) == 8:
            meld("ok", f"Fixtures aanwezig ({naam})", "8 bestanden")
        else:
            meld("fout", f"Fixtures aanwezig ({naam})", f"{len(bestanden)} van 8 gevonden")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        bezet = s.connect_ex(("127.0.0.1", port)) == 0
    if bezet:
        meld("let op", f"Poort {port} vrij", "in gebruik — kies een andere met --port")
    else:
        meld("ok", f"Poort {port} vrij", "")


# ---------------------------------------------------------------------------
# 2. De federation API
# ---------------------------------------------------------------------------
def check_federatie(base: str) -> bool:
    kop(f"2. Federation API  ({base})")

    host = urllib.parse.urlparse(base).hostname
    try:
        adres = socket.gethostbyname(host)
        meld("ok", "Hostnaam resolvet", f"{host} -> {adres}")
    except OSError:
        meld("fout", "Hostnaam resolvet", f"{host} onbekend — ontbreekt die in /etc/hosts?")
        return False

    status, body = haal(f"{base}/docs", timeout=10)
    if status == 200:
        meld("ok", "API bereikbaar (/docs)", "HTTP 200")
        return True
    if status is None:
        meld("fout", "API bereikbaar (/docs)", body.decode()[:60])
    else:
        meld("fout", "API bereikbaar (/docs)", f"HTTP {status} — draait de federation-pod?")
    return False


# ---------------------------------------------------------------------------
# 3. De eigen EHRbase achter die API
# ---------------------------------------------------------------------------
def check_ehrbase(base: str, key: str):
    kop("3. Eigen EHRbase")

    vraag = urllib.parse.urlencode({"query": "SELECT COUNT(e/ehr_id/value) FROM EHR e"})
    status, body = haal(f"{base}/own-data/query?{vraag}", key=key, timeout=30)

    if status == 200:
        try:
            aantal = json.loads(body).get("rows", [[None]])[0][0]
            meld("ok", "EHRbase antwoordt", f"{aantal} EHR's in de eigen node")
        except Exception:
            meld("ok", "EHRbase antwoordt", "HTTP 200")
    elif status == 401:
        meld("fout", "EHRbase antwoordt", "HTTP 401 — de API-key hoort niet bij deze node")
    elif status == 503:
        meld("fout", "EHRbase antwoordt", "HTTP 503 — API draait, EHRbase onbereikbaar")
    else:
        meld("fout", "EHRbase antwoordt", f"HTTP {status}")


# ---------------------------------------------------------------------------
# 4. De vier data-endpoints
# ---------------------------------------------------------------------------
def check_endpoints(base: str, key: str, btg_key: str, bsn: str):
    for label, gebruikte_key in (("zonder break-the-glass", key), ("met break-the-glass", btg_key)):
        kop(f"4. Data-endpoints — {label}")
        nodes_gezien = set()

        for endpoint in ENDPOINTS:
            qs = urllib.parse.urlencode({"bsn": bsn, "requester": "controle"})
            status, body = haal(f"{base}/{endpoint}?{qs}", key=gebruikte_key, timeout=60)

            if status not in (200, 503):
                detail = f"HTTP {status}" if status else body.decode()[:50]
                meld("fout", f"/{endpoint}", detail)
                continue

            try:
                payload = json.loads(body)
            except Exception:
                meld("fout", f"/{endpoint}", "onleesbare JSON")
                continue

            successen = payload.get("successes", payload if "failures" not in payload else {})
            mislukt = payload.get("failures", {})
            per_node = {n.removesuffix("_federation"): len(v) for n, v in successen.items()}
            nodes_gezien.update(per_node)
            nodes_gezien.update(n.removesuffix("_federation") for n in mislukt)

            totaal = sum(per_node.values())
            samenvatting = ", ".join(f"{n}: {a}" for n, a in sorted(per_node.items())) or "geen"
            if mislukt:
                samenvatting += f"  |  onbereikbaar: {', '.join(sorted(n.removesuffix('_federation') for n in mislukt))}"

            if totaal:
                meld("ok", f"/{endpoint}", samenvatting)
            elif mislukt:
                meld("fout", f"/{endpoint}", samenvatting)
            else:
                meld("let op", f"/{endpoint}", "0 records — klopt het BSN, of blokkeert consent?")

        if nodes_gezien:
            print(f"  {GRIJS}     nodes in de federatie: {', '.join(sorted(nodes_gezien))}{RESET}")


def main():
    p = argparse.ArgumentParser(description="Controleert of deze machine de DABS demo kan draaien")
    # ZIO is de eigen node: de demo draait daar, dus bevragen we die federation API.
    p.add_argument("--federation-base", default="http://federation.zio.local.dh.unimaas.nl")
    p.add_argument("--key", default="key1")
    p.add_argument("--btg-key", default="btgkey1")
    p.add_argument("--bsn", default="999990603")
    p.add_argument("--port", type=int, default=8800)
    args = p.parse_args()

    base = args.federation_base.rstrip("/")

    print("\nDABS demo — omgevingscontrole")
    check_machine(args.port)

    if check_federatie(base):
        check_ehrbase(base, args.key)
        check_endpoints(base, args.key, args.btg_key, args.bsn)
    else:
        kop("3 en 4 overgeslagen")
        print(f"  {GRIJS}De federation API is niet bereikbaar, dus de endpoints zijn niet te testen.")
        print(f"  De demo draait ondertussen gewoon op fixtures: python3 server.py{RESET}")

    fouten = resultaten.count("fout")
    waarschuwingen = resultaten.count("let op")
    print()
    if fouten:
        print(f"{ROOD}{fouten} controle(s) mislukt{RESET}, {waarschuwingen} waarschuwing(en).")
        print(f"{GRIJS}De demo draait hoe dan ook op fixtures: python3 server.py --dataset rich{RESET}\n")
        return 1
    print(f"{GROEN}Alles in orde{RESET}" + (f", {waarschuwingen} waarschuwing(en)" if waarschuwingen else "") + ".\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
