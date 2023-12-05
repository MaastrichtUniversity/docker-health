"""
Functions to POST a composition to EHRbase
"""

import os
import json
from datetime import datetime
from uuid import UUID
import requests

EHRBASE_USERRNAME = os.environ["EHRBASE_USERRNAME"]
EHRBASE_PASSWORD = os.environ["EHRBASE_PASSWORD"]
EHRBASE_BASE_URL = os.environ["EHRBASE_BASE_URL"]
ECIS_BASE_URL = os.environ["ECIS_BASE_URL"]

def post_composition(ehr_id: UUID, composition: dict) -> UUID:
    """
    Post a composition to the server
    Parameters
    ----------
    ehr_id: UUID
        ehr_id for patient
    composition: dict
        Composition to be posted


    Returns
    -------
    UUID
        versioned id for this composition

    """
    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition"
    headers = {
        # "Accept": "application/json; charset=UTF-8",
        # "Prefer": "return=representation",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=json.dumps(composition),
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    response_json = json.loads(response.text)
    print(f"RESPONSE: {response.status_code}")
    if response.ok:
        print(f"Composition was successfully created")
        return response_json["uid"]["value"]
    else:
        print(f'ERROR {response_json["error"]}')
        print(response_json["message"])
        return None


def post_flat_composition(ehr_id: UUID, template_id: str, flat_composition: dict) -> UUID:
    """
    Post a flat composition to the server
    Parameters
    ----------
    ehr_id: UUID
        ehr_id for patient
    template_id: str
        identifier of the template
    composition: dict
        flat Composition to be posted


    Returns
    -------
    UUID
        versioned id for this composition

    """
    url = f"{ECIS_BASE_URL}/composition/?format=FLAT&ehrId={ehr_id}&templateId={template_id}"

    headers = {
        # "Accept": "application/json; charset=UTF-8",
        # "Prefer": "return=representation",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=json.dumps(flat_composition),
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    response_json = json.loads(response.text)
    print(f"RESPONSE: {response.status_code}")
    if response.ok:
        print(f"Composition was successfully created")
        return response_json["uid"]["value"]
    else:
        print(f'ERROR {response_json["error"]}')
        print(response_json["message"])
        return None

def post_flat_composition_2(ehr_id: UUID, template_id: str, flat_composition: dict) -> UUID:
    """
    Post a flat composition to the server
    Parameters
    ----------
    ehr_id: UUID
        ehr_id for patient
    template_id: str
        identifier of the template
    composition: dict
        flat Composition to be posted


    Returns
    -------
    UUID
        versioned id for this composition

    """
    url = f"{ECIS_BASE_URL}/composition/?format=FLAT&ehrId={ehr_id}&templateId={template_id}"

    headers = {
        # "Accept": "application/json; charset=UTF-8",
        # "Prefer": "return=representation",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=json.dumps(flat_composition),
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    response_json = json.loads(response.text)
    print(f"RESPONSE: {response.status_code}")
    if response.ok:
        print(f"Composition was successfully created")
        return response_json["compositionUid"]
    else:
        print(f'ERROR {response_json["error"]}')
        print(response_json["message"])
        return None
