"""
Functions to transform and POST a composition to the EHRbase
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


def datetime_now() -> datetime:
    """Return current time on the NL time zone"""
    return datetime.now(NLTZ)


def transform_composition(simplified_composition: str, template_id: str) -> dict:
    """
    POST a simplified JSON composition to the Transformation REST API service
    and return the transformed composition according to the EHR standards

    Parameters
    ----------
    simplified_composition: str
        Simplified JSON composition to transform
    template_id: str
        Identifier of the template to use for the transformation

    Returns
    -------
    dict
        The transformed composition fitting EHR standards
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
        data=simplified_composition,
        timeout=10,
    )

    composition = response.json()
    # print(json.dumps(composition, indent=4))

    return composition


def post_composition(ehr_id: UUID, composition: dict) -> UUID | None:
    """
    POST a composition to the EHRbase server

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given patient
    composition: dict
        Composition to be posted

    Returns
    -------
    UUID
        versioned id of the composition, if response.ok is True
    None
        if reponse.ok is False
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


def write_json_composition(composition: str, json_filename: str):
    """
    Write a JSON composition to a file

    Parameters
    ----------
    composition: dict
        Composition to be posted
    json_filename: str
        Name of the file to create
    """
    with open(json_filename, 'w', encoding='utf-8') as file:
        json.dump(composition, file, indent=4)
