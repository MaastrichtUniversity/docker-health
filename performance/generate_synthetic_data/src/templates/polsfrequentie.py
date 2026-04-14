from src.utils import (
    generate_random_full_date,
    generate_random_integer,
    generate_random_string,
    generate_random_coded_value,
    optional,
)

POLS_REGELMATIGHEID_CODED_LIST = [
    "Regelmatige pulsaties",
    "Onregelmatige pulsaties",
]

def generate_synthetic_polsfrequentie(bsn):
    return {
        "BSN": bsn,
        "POLSFREQUENTIE_WAARDE (/min)": generate_random_integer(0, 999),
        "POLSFREQUENTIE_DATUM_TIJD": generate_random_full_date(),
        "TOELICHTING": optional(generate_random_string(), p=0.5),
        "POLS_REGELMATIGHEID": optional(generate_random_coded_value(POLS_REGELMATIGHEID_CODED_LIST), p=0.7),
        "DATE_TIME": generate_random_full_date(),
    }
