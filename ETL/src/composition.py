"""
Functions to POST a composition to EHRbase
"""

import json
import os
from datetime import datetime
from uuid import UUID

import pytz
import requests

NLTZ = pytz.timezone('Europe/Amsterdam')
EHRBASE_USERRNAME = os.environ['EHRBASE_USERRNAME']
EHRBASE_PASSWORD = os.environ['EHRBASE_PASSWORD']
EHRBASE_BASE_URL = os.environ['EHRBASE_BASE_URL']


def post_composition(ehr_id: UUID, composition: dict) -> UUID:
    """
    Post a composition to the server
    Parameters
    ----------
    ehr_id: UUID
        ehr_id for patient
    composition: dict
        Compistion to be posted


    Returns
    -------
    UUID
        versioned id for this composition

    """
    # print(json.dumps(composition))
    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition"
    headers = {
        'Accept': 'application/json; charset=UTF-8',
        'Prefer': 'return=representation',
        'Content-Type': 'application/json',
    }
    response = requests.request(
        'POST',
        url,
        headers=headers,
        data=json.dumps(composition),
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    response_json = json.loads(response.text)
    print(f"RESPONSE: {response.status_code}")
    if response.ok:
        print("Composition was successfully created")
        return response_json['uid']['value']
    print(f"ERROR {response_json['error']}")
    print(response_json['message'])
    return None


def transform_composition(composition: str, template_id: str) -> dict:
    """
    Post a composition to the Transformation REST API service.

    Parameters
    ----------
    composition
    template_id

    Returns
    -------
    dict
        The transformed EHR composition
    """
    url = f"http://transform.dh.local:8080/{template_id}"
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }
    response = requests.request(
        'POST',
        url,
        headers=headers,
        data=composition,
        timeout=10,
    )

    result = response.json()

    # print(json.dumps(result, indent=4))

    return result

def write_json_composition(composition: str, json_filename: str):
    """
    TODO
    """
    with open(json_filename, 'w') as file:
        json.dump(composition, file, indent=4)


def datetime_now() -> datetime:
    """Return current time on the NL timezone"""
    return datetime.now(NLTZ)
