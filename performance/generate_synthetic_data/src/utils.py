import string
from enum import StrEnum
from datetime import datetime, timedelta
from numpy.random import randint, choice
from faker import Faker

FAKE = Faker("nl_NL")


class InputTemplateID(StrEnum):
    WOONSITUATIE_2024 = "woonsituatie_2024"
    POLSFREQUENTIE_2024 = "polsfrequentie_2024"


def generate_bsn(used_bsn):
    while True:
        bsn = FAKE.ssn()
        if bsn not in used_bsn:
            return bsn


def optional(value, p):
    return choice([value, None], p=[p, 1 - p])


def generate_random_full_date(start_date=datetime(2020, 1, 1), end_date=datetime(2026, 12, 31)):
    delta = end_date - start_date
    random_days = randint(0, delta.days)
    random_seconds = randint(0, 86399)  # Seconds in a day
    date = start_date + timedelta(days=random_days, seconds=random_seconds)
    return date.strftime("%Y-%m-%dT%H:%M:%S")


def generate_random_date(start_date=datetime(2020, 1, 1), end_date=datetime(2026, 12, 31), p_partial=[0.7, 0.2, 0.1]):
    delta = end_date - start_date
    random_days = randint(0, delta.days)
    date = start_date + timedelta(days=random_days)
    format = choice(["yyyy-mm-dd", "yyyy-mm", "yyyy"], p=p_partial)
    if format == "yyyy-mm-dd":
        return date.strftime("%Y-%m-%d")
    elif format == "yyyy-mm":
        return date.strftime("%Y-%m")
    else:
        return date.strftime("%Y")


def generate_random_string(min_len=5, max_len=50):
    chars = list(string.ascii_lowercase)
    length = randint(min_len, max_len + 1)
    random_chars = choice(chars, size=length)
    return "".join(random_chars)


def generate_random_integer(min_value, max_value):
    return randint(min_value, max_value)


def generate_random_coded_value(coded_list):
    return str(choice(coded_list))
