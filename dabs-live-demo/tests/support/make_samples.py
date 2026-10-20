"""Regenerate ``tests/samples/*.json`` from ``docs/federation-samples.md``.

Test-only helper; nothing in the application imports it. Running it rewrites the four
sample files deterministically. Verbatim records are copied field-for-field from the
samples doc; the extra records needed to reach the documented 24/24 counts are generated
here. See ``tests/samples/README.md`` for the verbatim/generated breakdown.

    python3 tests/support/make_samples.py
"""

import json
import pathlib
from collections import Counter

OUT = pathlib.Path(__file__).resolve().parents[1] / "samples"
OUT.mkdir(parents=True, exist_ok=True)


def coded(value, code, terminology):
    return {"Value": value, "Code": code, "Terminology": terminology}


# ---------------------------------------------------------------------------
# Patient -- zio verbatim, the other three structurally identical per the doc.
# ---------------------------------------------------------------------------
PATIENT_ZIO = {
    "SystemId": "DEMO_DATA",
    "Provider": "zio",
    "StartTime": "2024-10-10T10:10:10.41",
    "Naamgegevens": {
        "Voornamen": "Johanna Petronella Maria",
        "Initialen": "J.P.M.",
        "Roepnaam": "Jo",
        "Naamgebruik": {"Value": "Eigen geslachtsnaam", "Code": "NL1", "Terminology": "NaamGebruik"},
        "Voorvoegsels": "van",
        "Achternaam": "Putten",
        "VoorvoegselsPartner": "van der",
        "AchternaamPartner": "Giessen",
        "Titels": "Prof",
    },
    "Adresgegevens": [
        {
            "Straat": "1e Jacob van Campenstr",
            "Huisnummer": "15",
            "Huisnummerletter": "BV",
            "Huisnummertoevoeging": "TG",
            "AanduidingBijNummer": {"Value": "Bij", "Code": "by",
                                    "Terminology": "AanduidingBijHuisnummer & NullFlavor"},
            "Woonplaats": "Hoogmade",
            "Gemeente": "Kaag en Braassem",
            "Postcode": "1012 NX",
            "Land": {"Value": "Nederland", "Code": "NL",
                     "Terminology": "ISO 3166-1 alpha-2 & NullFlavor"},
            "AdresSoort": {"Value": "Visit Address", "Code": "PHYS",
                           "Terminology": "AddressUse & NullFlavor"},
            "AdditioneleInformatie": "Data Max",
        }
    ],
    "Contactgegevens": {
        "Telefoonnummers": [
            {
                "Telefoonnummer": "31611234568",
                "NummerSoort": {"Value": "Work Place", "Code": "WP",
                                "Terminology": "AddressUse & NullFlavor"},
                "TelecomType": {"Value": "Mobile Contact", "Code": "MC",
                                "Terminology": "TelecomDeviceTypes & AddressUse & NullFavor"},
                "Toelichting": "c",
            }
        ],
        "EmailAdressen": [
            {"EmailAdres": "giesput@myweb.nl",
             "EmailSoort": {"Value": "Primary Home", "Code": "HP",
                            "Terminology": "AddressUse & NullFlavor"}}
        ],
    },
    "Identificatienummer": ["999990603"],
    "Geboortedatum": "1984-10-03",
    "MeerlingIndicator": False,
    "MeerlingVolgorde": None,
    "Geslacht": {"Value": "Unknown", "Code": "UNK",
                 "Terminology": "http://terminology.hl7.org/CodeSystem/v3-NullFlavor"},
    "Genderidentiteit": {"Value": "Non-binaire genderidentiteit", "Code": "33791000087105",
                         "Terminology": "SNOMED CT & NullFlavor"},
    "OverlijdensIndicator": {"Value": "Dead", "Code": "at0006", "Terminology": "local"},
    "DatumOverlijden": "2042-01-01",
}

PATIENT_START = {
    "envida": "2023-11-18T15:30:12.123",
    "mumc": "2023-11-14T15:50:14.321",
    "vitala": "2023-11-14T15:50:14.321",
}

patient = [PATIENT_ZIO]
for node, start in PATIENT_START.items():
    rec = json.loads(json.dumps(PATIENT_ZIO))
    rec["Provider"] = node
    rec["StartTime"] = start
    patient.append(rec)

# ---------------------------------------------------------------------------
# Bloeddruk -- verbatim representative records for zio/envida/vitala; rest generated.
# ---------------------------------------------------------------------------
BP_ZIO = {
    "SystemId": "DEMO_DATA", "Provider": "zio", "StartTime": "2018-08-11T00:00:00",
    "ManchetType": None,
    "Meetmethode": coded("Non-invasief", "22762002", "SNOMED CT & NullFlavor"),
    "SystolischeBloeddruk": {"Magnitude": 139, "Units": "mm[Hg]"},
    "DiastolischeBloeddruk": {"Magnitude": 85, "Units": "mm[Hg]"},
    "GemiddeldeBloeddruk": None, "BloeddrukDatumTijd": "2018-08-11T00:00:00",
    "Toelichting": None,
    "AnatomischeLocatie": {
        "Locatie": coded("Structuur van linker bovenarm", "368208006", "SNOMED CT & NullFlavor"),
        "Lateraliteit": coded("Links", "7771000", "SNOMED CT"),
    },
    "Houding": coded("Zittende positie", "33586001", "SNOMED CT & NullFlavor"),
    "DiastolischEindpunt": None,
}

BP_ENVIDA = {
    "SystemId": "DEMO_DATA", "Provider": "envida", "StartTime": "1983-03-16T15:34:59.427",
    "ManchetType": None, "Meetmethode": None,
    "SystolischeBloeddruk": {"Magnitude": 108, "Units": "mm[Hg]"},
    "DiastolischeBloeddruk": {"Magnitude": 73, "Units": "mm[Hg]"},
    "GemiddeldeBloeddruk": None, "BloeddrukDatumTijd": "2021-07-04T21:03:56.351",
    "Toelichting": None, "AnatomischeLocatie": None, "Houding": None,
    "DiastolischEindpunt": None,
}

BP_VITALA = {
    "SystemId": "DEMO_DATA", "Provider": "vitala", "StartTime": "2024-03-12T00:00:00",
    "ManchetType": None,
    "Meetmethode": coded("Non-invasief", "22762002", "SNOMED CT & NullFlavor"),
    "SystolischeBloeddruk": {"Magnitude": 121, "Units": "mm[Hg]"},
    "DiastolischeBloeddruk": {"Magnitude": 80, "Units": "mm[Hg]"},
    "GemiddeldeBloeddruk": None, "BloeddrukDatumTijd": "2024-03-12T00:00:00",
    "Toelichting": None,
    "AnatomischeLocatie": {
        "Locatie": coded("Structuur van bovenarm", "40983000", "SNOMED CT & NullFlavor"),
        "Lateraliteit": coded("Bilateraal", "51440002", "SNOMED CT"),
    },
    "Houding": coded("Zittende positie", "33586001", "SNOMED CT & NullFlavor"),
    "DiastolischEindpunt": None,
}

# generated series: (StartTime, BloeddrukDatumTijd, systolic, diastolic)
BP_SERIES = {
    "zio": [
        ("2017-05-02T00:00:00", "2017-05-02T00:00:00", 128, 79),
        ("2019-01-20T00:00:00", "2019-01-20T00:00:00", 135, 82),
        ("2020-11-05T00:00:00", "2020-11-05T00:00:00", 142, 88),
        ("2022-06-15T00:00:00", "2022-06-15T00:00:00", 130, 81),
        ("2023-09-07T00:00:00", "2023-09-07T00:00:00", 126, 78),
    ],
    "envida": [
        ("2016-02-11T00:00:00", "2016-02-11T00:00:00", 118, 74),
        ("2017-08-23T00:00:00", "2017-08-23T00:00:00", 121, 76),
        ("2019-04-14T00:00:00", "2019-04-14T00:00:00", 124, 77),
        ("2020-12-30T00:00:00", "2020-12-30T00:00:00", 127, 80),
        ("2022-10-19T00:00:00", "2022-10-19T00:00:00", 119, 75),
    ],
    "mumc": [
        ("2015-03-08T00:00:00", "2015-03-08T00:00:00", 132, 84),
        ("2016-07-21T00:00:00", "2016-07-21T00:00:00", 136, 86),
        ("2018-01-15T00:00:00", "2018-01-15T00:00:00", 141, 90),
        ("2019-09-27T00:00:00", "2019-09-27T00:00:00", 129, 83),
        ("2021-04-03T00:00:00", "2021-04-03T00:00:00", 134, 85),
        ("2023-02-18T00:00:00", "2023-02-18T00:00:00", 138, 87),
    ],
    "vitala": [
        ("2015-01-05T00:00:00", "2015-01-05T00:00:00", 115, 72),
        ("2016-11-11T00:00:00", "2016-11-11T00:00:00", 117, 74),
        ("2018-06-06T00:00:00", "2018-06-06T00:00:00", 123, 78),
        ("2020-02-02T00:00:00", "2020-02-02T00:00:00", 125, 79),
        ("2022-08-08T00:00:00", "2022-08-08T00:00:00", 120, 77),
    ],
}


def gen_bp(node, start, dt, sys_v, dia_v):
    loc = None
    if node == "zio":
        loc = {"Locatie": coded("Structuur van linker bovenarm", "368208006", "SNOMED CT & NullFlavor"),
               "Lateraliteit": coded("Links", "7771000", "SNOMED CT")}
    elif node == "mumc":
        loc = {"Locatie": coded("Structuur van rechter bovenarm", "368209003", "SNOMED CT & NullFlavor"),
               "Lateraliteit": coded("Rechts", "24028007", "SNOMED CT")}
    elif node == "vitala":
        loc = {"Locatie": coded("Structuur van bovenarm", "40983000", "SNOMED CT & NullFlavor"),
               "Lateraliteit": coded("Bilateraal", "51440002", "SNOMED CT")}
    houding = coded("Zittende positie", "33586001", "SNOMED CT & NullFlavor") if node != "envida" else None
    return {
        "SystemId": "DEMO_DATA", "Provider": node, "StartTime": start, "ManchetType": None,
        "Meetmethode": coded("Non-invasief", "22762002", "SNOMED CT & NullFlavor"),
        "SystolischeBloeddruk": {"Magnitude": sys_v, "Units": "mm[Hg]"},
        "DiastolischeBloeddruk": {"Magnitude": dia_v, "Units": "mm[Hg]"},
        "GemiddeldeBloeddruk": None, "BloeddrukDatumTijd": dt, "Toelichting": None,
        "AnatomischeLocatie": loc, "Houding": houding, "DiastolischEindpunt": None,
    }


blood_pressure = []
for node in ["zio", "envida", "mumc", "vitala"]:
    if node == "zio":
        blood_pressure.append(BP_ZIO)
    elif node == "envida":
        blood_pressure.append(BP_ENVIDA)
    elif node == "vitala":
        blood_pressure.append(BP_VITALA)
    for (start, dt, s, d) in BP_SERIES[node]:
        blood_pressure.append(gen_bp(node, start, dt, s, d))

# ---------------------------------------------------------------------------
# Lichaamsgewicht -- two verbatim representative records (zio, mumc); rest generated.
# ---------------------------------------------------------------------------
WEIGHT_ZIO = {
    "SystemId": "DEMO_DATA", "Provider": "zio", "StartTime": "2002-01-19T09:43:13.174",
    "GewichtWaarde": {"Magnitude": 85, "Units": "kg"},
    "GewichtDatumTijd": "2002-01-19T09:43:13.174", "Toelichting": None, "Kleding": None,
}
WEIGHT_MUMC = {
    "SystemId": "DEMO_DATA", "Provider": "mumc", "StartTime": "2023-09-10T00:00:00",
    "GewichtWaarde": {"Magnitude": 75.7, "Units": "kg"},
    "GewichtDatumTijd": "2023-09-10T00:00:00", "Toelichting": None,
    "Kleding": coded("Minimale kleding", "220121000146105", "ContextKleding & SNOMED CT"),
}

WEIGHT_SERIES = {
    "zio": [
        ("2010-02-02T00:00:00", 88.1, None),
        ("2014-06-14T00:00:00", 90.4, None),
        ("2018-03-03T00:00:00", 92.0, None),
        ("2021-01-11T00:00:00", 89.5, None),
        ("2023-12-12T00:00:00", 87.2, coded("Minimale kleding", "220121000146105", "ContextKleding & SNOMED CT")),
    ],
    "envida": [
        ("2009-05-05T00:00:00", 64.0, None),
        ("2013-09-09T00:00:00", 67.3, None),
        ("2017-04-04T00:00:00", 70.5, None),
        ("2020-08-08T00:00:00", 72.8, None),
        ("2022-11-11T00:00:00", 71.4, None),
        ("2024-01-01T00:00:00", 70.9, coded("Minimale kleding", "220121000146105", "ContextKleding & SNOMED CT")),
    ],
    "mumc": [
        ("2008-01-01T00:00:00", 61.2, None),
        ("2012-03-03T00:00:00", 65.8, None),
        ("2016-07-07T00:00:00", 69.0, None),
        ("2019-10-10T00:00:00", 73.4, None),
        ("2024-01-20T00:00:00", 76.2, None),
    ],
    "vitala": [
        ("2011-02-02T00:00:00", 55.5, None),
        ("2015-05-05T00:00:00", 58.9, None),
        ("2018-08-08T00:00:00", 62.1, None),
        ("2021-11-11T00:00:00", 65.0, None),
        ("2024-02-02T00:00:00", 66.6, None),
        ("2025-06-06T00:00:00", 67.1, None),
    ],
}


def gen_weight(node, dt, mag, kleding):
    return {
        "SystemId": "DEMO_DATA", "Provider": node, "StartTime": dt,
        "GewichtWaarde": {"Magnitude": mag, "Units": "kg"},
        "GewichtDatumTijd": dt, "Toelichting": None, "Kleding": kleding,
    }


weight = []
for node in ["zio", "envida", "mumc", "vitala"]:
    if node == "zio":
        weight.append(WEIGHT_ZIO)
    elif node == "mumc":
        weight.append(WEIGHT_MUMC)
    for (dt, mag, kleding) in WEIGHT_SERIES[node]:
        weight.append(gen_weight(node, dt, mag, kleding))

# ---------------------------------------------------------------------------
# LichaamsLengte -- all four records verbatim from the doc.
# ---------------------------------------------------------------------------
length = [
    {
        "SystemId": "DEMO_DATA", "Provider": "zio", "StartTime": "2001-03-19T11:43:13.174",
        "LengteWaarde": {"Magnitude": 184, "Units": "cm"},
        "LengteDatumTijd": "2001-03-19T10:43:13.174", "Toelichting": "Zonder schoenen",
        "Positie": coded("Liggende positie", "102538003", "SNOMED CT"),
    },
    {
        "SystemId": "DEMO_DATA", "Provider": "envida", "StartTime": "2001-03-19T11:43:13.174",
        "LengteWaarde": {"Magnitude": 199, "Units": "cm"},
        "LengteDatumTijd": "2001-03-19T10:43:13.174", "Toelichting": "Zonder schoenen",
        "Positie": coded("Liggende positie", "102538003", "SNOMED CT"),
    },
    {
        "SystemId": "DEMO_DATA", "Provider": "mumc", "StartTime": "2002-01-19T09:43:13.174",
        "LengteWaarde": {"Magnitude": 120, "Units": "cm"},
        "LengteDatumTijd": "2002-01-19T09:43:13.174", "Toelichting": None,
        "Positie": coded("Other", "OTH", "SNOMED CT"),
    },
    {
        "SystemId": "DEMO_DATA", "Provider": "vitala", "StartTime": "2001-03-19T11:43:13.174",
        "LengteWaarde": {"Magnitude": 199, "Units": "cm"},
        "LengteDatumTijd": "2001-03-19T10:43:13.174", "Toelichting": "Zonder schoenen",
        "Positie": coded("Liggende positie", "102538003", "SNOMED CT"),
    },
]

FILES = [("Patient", patient), ("Bloeddruk", blood_pressure),
         ("Lichaamsgewicht", weight), ("LichaamsLengte", length)]

for name, data in FILES:
    (OUT / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                      encoding="utf-8")
    print(f"{name}: {len(data)} records, per node {dict(Counter(r['Provider'] for r in data))}")
