"""Genereert de fixture-sets voor de DABS demo.

PERSPECTIEF: ZIO. De UI is een applicatie van ZIO-medewerkers. Zij hebben altijd toegang
tot hun eigen data; gegevens van andere zorgaanbieders komen pas in beeld wanneer daar
toestemming voor is, of na break-the-glass.

Dat levert deze twee varianten op:

* ``<endpoint>.json``      - alleen ZIO. De eigen node, altijd toegankelijk.
* ``<endpoint>.btg.json``  - ZIO plus alle andere nodes.

LET OP - dit is een demomodel, niet letterlijk wat de API met deze demodata doet.
In ``test_federation_rest.py`` heeft patient 999990603 bij MUMC consent = true (regel 248),
waardoor MUMC vanuit ZIO ook zonder break-the-glass zou meekomen; ``TestZioClient`` gebruikt
daarom de break-the-glass-verwachtingen als gewone uitkomst. Dat is een eigenaardigheid van
deze demodataset, niet van het privacymodel. Voor de showcase modelleren we het algemene
geval - eigen node altijd, andere nodes achter toestemming - omdat juist dat de werking van
break-the-glass laat zien. Met ``--mode live`` telt wat de nodes echt teruggeven.

Twee sets:

* ``fixtures/``      - getrouw. Exact de records die de federation API teruggeeft voor
                       BSN 999990603, overgenomen uit ``test_federation_rest.py``.
                       Weinig meetpunten, want zo ziet de echte demodata eruit.
* ``fixtures-rich/`` - verrijkt. Dezelfde patient met een langere meetreeks zodat de
                       grafieken tijdens een showcase iets te laten zien hebben.
                       Dit is GEEN brondata; de UI labelt deze set als zodanig.

Alleen MUMC en ZIO, want dat zijn de nodes die draaien.

Herbouwen:  python3 tools/make_fixtures.py
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BSN = "999990603"


def bloeddruk(sys_, dia, when, provider, system_id, houding=None, locatie=None):
    return {
        "manchet_type": None,
        "meetmethode": None,
        "systolische_bloeddruk": sys_,
        "diastolische_bloeddruk": dia,
        "gemiddelde_bloeddruk": None,
        "bloeddruk_datum_tijd": when,
        "toelichting": None,
        "anatomische_locatie": {"locatie": locatie, "lateraliteit": None} if locatie else None,
        "houding": houding,
        "diastolisch_eindpunt": None,
        "system_id": system_id,
        "provider": provider,
        "start_time": when,
    }


def gewicht(kg, when, provider, system_id):
    return {
        "gewichtwaarde_magnitude": kg,
        "gewichtwaarde_units": "kg",
        "gewicht_datum_tijd": when,
        "toelichting": None,
        "kleding": None,
        "system_id": system_id,
        "provider": provider,
        "start_time": when,
    }


def lengte(cm, when, provider, system_id, positie=None, toelichting=None):
    return {
        "lengtewaarde_magnitude": cm,
        "lengtewaarde_units": "cm",
        "lengte_datum_tijd": when,
        "toelichting": toelichting,
        "positie": positie,
        "system_id": system_id,
        "provider": provider,
        "start_time": when,
    }


# --------------------------------------------------------------------------
# Patientgegevens - de twee bronnen zijn het oneens over deze patient.
# Dat is echte brondata en blijft in beide sets ongewijzigd staan.
#
# `_veld_gewijzigd` is GEEN brondata. De PatientDTO2024 kent maar een tijdstempel
# (`start_time`, hier gelijk aan de geboortedatum), dus per-veld-recentheid is uit de
# federation API niet af te leiden. Voor de demo modelleren we per veld wanneer het in
# dat bronsysteem voor het laatst is bijgewerkt, zodat het dashboard per variabele de
# nieuwste waarde kan kiezen. Zodra de bron zulke tijdstempels wel levert, gebruikt de
# frontend die zonder codewijziging. Met de schakelaar "alleen brondata" verdwijnt dit
# veld volledig, want dan wordt er rechtstreeks bij de endpoints opgehaald.
# --------------------------------------------------------------------------
GEWIJZIGD_MUMC = {
    "naam": "2024-06-04",
    "geboortedatum": "2024-01-24",
    "geslacht": "2024-01-24",
    "identificatienummer": "2022-05-11",
    "adres": "2023-02-14",
    "telefoon": "2021-06-30",
    "email": "2023-09-01",
    "overleden": "2024-06-04",
}

GEWIJZIGD_ZIO = {
    "naam": "2019-01-10",
    "geboortedatum": "2018-08-11",
    "geslacht": "2025-01-01",
    "identificatienummer": "2025-01-01",
    "adres": "2025-03-14",
    "telefoon": "2024-11-02",
    "overleden": "2025-01-01",
}

PATIENT_MUMC = {
    "naamgegevens": {
        "voornamen": "B.E.A.C.O.N.T.W.O.P.",
        "initialen": None,
        "roepnaam": None,
        "naamgebruik": None,
        "voorvoegsels": None,
        "achternaam": "Berken van der",
        "voorvoegsels_partner": None,
        "achternaam_partner": None,
        "titels": None,
    },
    "adresgegevens": [
        {
            "straat": "Goatstraat",
            "huisnummer": "500",
            "huisnummerletter": None,
            "huisnummertoevoeging": None,
            "aanduiding_bij_nummer": None,
            "woonplaats": "s-Hertogenbosch",
            "gemeente": None,
            "postcode": "4269 VA",
            "land": None,
            "adres_soort": None,
            "additionele_informatie": None,
        }
    ],
    "contactgegevens": {
        "telefoonnummers": [
            {"telefoonnummer": "(026) 292 69 00", "nummer_soort": None, "telecom_type": None, "toelichting": None}
        ],
        "email_adressen": [{"email_adres": "look@this.com", "email_soort": None}],
    },
    "identificatienummer": [BSN],
    "geboortedatum": "1996-03-19",
    "meerling_indicator": False,
    "meerling_volgorde": None,
    "geslacht": "Male",
    "genderidentiteit": None,
    "overlijdens_indicator": False,
    "datum_overlijden": None,
    "system_id": "EPIC",
    "provider": "mumc",
    "start_time": "1996-03-19T00:00:00",
    "_veld_gewijzigd": GEWIJZIGD_MUMC,
}

PATIENT_ZIO = {
    "naamgegevens": {
        "voornamen": "Marieke",
        "initialen": "J.P.M.",
        "roepnaam": None,
        "naamgebruik": None,
        "voorvoegsels": "van",
        "achternaam": "Putten",
        "voorvoegsels_partner": "van der",
        "achternaam_partner": "Giessen",
        "titels": None,
    },
    "adresgegevens": [
        {
            "straat": "Begijnekade",
            "huisnummer": "13",
            "huisnummerletter": None,
            "huisnummertoevoeging": "TG",
            "aanduiding_bij_nummer": None,
            "woonplaats": "Utrecht",
            "gemeente": None,
            "postcode": "3512VV",
            "land": None,
            "adres_soort": None,
            "additionele_informatie": None,
        }
    ],
    "contactgegevens": {
        "telefoonnummers": [
            {"telefoonnummer": "624310831", "nummer_soort": None, "telecom_type": None, "toelichting": None}
        ],
        "email_adressen": [],
    },
    "identificatienummer": [BSN, "10009"],
    "geboortedatum": "1985-07-18",
    "meerling_indicator": False,
    "meerling_volgorde": None,
    "geslacht": "Unknown",
    "genderidentiteit": None,
    "overlijdens_indicator": False,
    "datum_overlijden": None,
    "system_id": "Tetra",
    "provider": "zio",
    "start_time": "1985-07-18T00:00:00",
    "_veld_gewijzigd": GEWIJZIGD_ZIO,
}


# --------------------------------------------------------------------------
# Getrouwe set
# --------------------------------------------------------------------------
FAITHFUL = {
    "Bloeddruk": {
        "mumc": [
            bloeddruk(109, 75, "2024-06-04T20:51:14", "mumc", "EPIC",
                      houding="Gekantelde positie", locatie="Structuur van linker bovenarm")
        ],
        "zio": [bloeddruk(139, 85, "2018-08-11T00:00:00", "zio", "Tetra")],
    },
    "Lichaamsgewicht": {
        "mumc": [gewicht(81, "2024-01-24T14:54:00", "mumc", "EPIC")],
        "zio": [gewicht(74, "2025-01-01T00:00:00", "zio", "Tetra")],
    },
    "LichaamsLengte": {
        "mumc": [
            lengte(183, "2024-01-24T14:54:00", "mumc", "EPIC"),
            lengte(180, "2024-04-04T14:00:00", "mumc", "EPIC"),
        ],
        "zio": [lengte(181, "2025-01-01T00:00:00", "zio", "Tetra")],
    },
    "Patient": {"mumc": [PATIENT_MUMC], "zio": [PATIENT_ZIO]},
}


# --------------------------------------------------------------------------
# Verrijkte set - langere reeksen, zodat de grafieken een verloop tonen.
# --------------------------------------------------------------------------
_MUMC_BP = [
    (128, 84, "2023-02-14T09:20:00"),
    (134, 88, "2023-06-27T11:05:00"),
    (131, 86, "2023-11-09T14:40:00"),
    (126, 82, "2024-01-24T14:54:00"),
    (109, 75, "2024-06-04T20:51:14"),
    (118, 79, "2024-10-15T10:15:00"),
    (122, 81, "2025-02-03T08:50:00"),
    (117, 77, "2025-06-18T13:30:00"),
]
_ZIO_BP = [
    (139, 85, "2018-08-11T00:00:00"),
    (145, 92, "2019-05-22T00:00:00"),
    (142, 89, "2021-03-17T00:00:00"),
    (136, 87, "2023-09-05T00:00:00"),
    (133, 84, "2024-08-20T00:00:00"),
    (129, 83, "2025-01-01T00:00:00"),
]
_MUMC_KG = [
    (88.4, "2023-02-14T09:20:00"),
    (86.1, "2023-06-27T11:05:00"),
    (84.7, "2023-11-09T14:40:00"),
    (81.0, "2024-01-24T14:54:00"),
    (80.2, "2024-10-15T10:15:00"),
    (79.5, "2025-06-18T13:30:00"),
]
_ZIO_KG = [
    (82.0, "2019-05-22T00:00:00"),
    (79.3, "2021-03-17T00:00:00"),
    (76.8, "2023-09-05T00:00:00"),
    (75.1, "2024-08-20T00:00:00"),
    (74.0, "2025-01-01T00:00:00"),
]

RICH = {
    "Bloeddruk": {
        "mumc": [
            bloeddruk(s, d, t, "mumc", "EPIC",
                      houding="Gekantelde positie" if t.startswith("2024-06") else None,
                      locatie="Structuur van linker bovenarm" if t.startswith("2024-06") else None)
            for s, d, t in _MUMC_BP
        ],
        "zio": [bloeddruk(s, d, t, "zio", "Tetra") for s, d, t in _ZIO_BP],
    },
    "Lichaamsgewicht": {
        "mumc": [gewicht(kg, t, "mumc", "EPIC") for kg, t in _MUMC_KG],
        "zio": [gewicht(kg, t, "zio", "Tetra") for kg, t in _ZIO_KG],
    },
    "LichaamsLengte": FAITHFUL["LichaamsLengte"],
    "Patient": FAITHFUL["Patient"],
}


def write_set(target: pathlib.Path, data: dict):
    """Schrijft per endpoint twee bestanden: normaal en break-the-glass.

    Zonder break-the-glass alleen ZIO: de eigen node, waar ZIO-medewerkers altijd bij
    mogen. MUMC komt als lege lijst terug, wat het dashboard toont als "geen toestemming".
    Met break-the-glass vervalt het consent-filter en verschijnt MUMC erbij.
    """
    target.mkdir(parents=True, exist_ok=True)
    for endpoint, per_node in data.items():
        # Eigen node eerst, zoals de federation API hem ook als eerste teruggeeft.
        normaal = {"zio_federation": per_node["zio"], "mumc_federation": []}
        btg = {"zio_federation": per_node["zio"], "mumc_federation": per_node["mumc"]}
        (target / f"{endpoint}.json").write_text(json.dumps(normaal, indent=2, ensure_ascii=False))
        (target / f"{endpoint}.btg.json").write_text(json.dumps(btg, indent=2, ensure_ascii=False))
        print(f"  {target.name}/{endpoint}: {len(per_node['zio'])} zio (eigen), "
              f"+{len(per_node['mumc'])} mumc na break-the-glass")


if __name__ == "__main__":
    print("Getrouwe set:")
    write_set(ROOT / "fixtures", FAITHFUL)
    print("Verrijkte set:")
    write_set(ROOT / "fixtures-rich", RICH)
    print("\nKlaar.")
