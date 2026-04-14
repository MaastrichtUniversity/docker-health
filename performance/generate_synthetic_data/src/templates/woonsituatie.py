from src.utils import (
    generate_random_full_date,
    generate_random_date,
    generate_random_string,
    generate_random_coded_value,
    optional,
)

WONING_TYPE_CODED_LIST = [
    "Bovenwoning",
    "Benedenwoning",
    "Eengezinswoning",
    "Appartement of flatwoning",
    "Aanleunwoning",
    "Woonboot",
    "Woonwagen",
    "Instelling WLZ",
    "Instelling ZVW",
    "Instelling WMO",
    "Asielzoekers-centrum",
    "Dakloos",
    "Justitiële Inrichting",
    "Other",
]

WONING_AANPASSING_CODED_LIST = [
    "Badstoel en/of douchestoel",
    "Traplift",
    "Aangepast toilet",
    "Aangepast bed",
    "Woningaanpassing",
    "Wandbeugel",
    "Other",
]

WOON_OMSTANDIGHEID_CODED_LIST = [
    "Huis bevat trap",
    "Woont in appartement met lift",
    "Toegang tot woning via trap",
    "Ingang van woning geblokkeerd",
    "Huis bevat structurele belemmering voor verplaatsing",
    "Rommelige leefruimte",
    "Vieze leefomstandigheden",
    "Houdt huisdieren",
    "Vloerbedekking onveilig",
    "Other",
]


def generate_synthetic_woonsituatie(bsn):
    return {
        "BSN": bsn,
        "DATUM": optional(generate_random_date(p_partial=[0.2, 0.5, 0.3]), p=0.7),
        "WONING_TYPE": optional(generate_random_coded_value(WONING_TYPE_CODED_LIST), p=0.9),
        "WONING_AANPASSING": optional(generate_random_coded_value(WONING_AANPASSING_CODED_LIST), p=0.6),
        "WOON_OMSTANDIGHEID": optional(generate_random_coded_value(WOON_OMSTANDIGHEID_CODED_LIST), p=0.6),
        "TOELICHTING": optional(generate_random_string(), p=0.4),
        "DATE_TIME": generate_random_full_date(),
    }
