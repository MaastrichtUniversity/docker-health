"""
Functions to POST and GET EHR from the EHRbase
"""

import os
import json
from typing import List
from uuid import UUID
import requests

EHRBASE_USERRNAME = os.environ["EHRBASE_USERRNAME"]
EHRBASE_PASSWORD = os.environ["EHRBASE_PASSWORD"]
EHRBASE_BASE_URL = os.environ["EHRBASE_BASE_URL"]


def get_ehr_id_for_patient_id(patient_id: str) -> None | UUID:
    """
    Get the ehr_id for a patient given the patient external id

    Parameters
    ----------
    patient_id: str
        External patient id

    Returns
    -------
    UUID
        ehr_id if the patient already has an EHR (code error 404)
    None
        If the patient does not have an ehr
    """
    url = f"{EHRBASE_BASE_URL}/ehr"
    myparams = {"subject_id": patient_id, "subject_namespace": "datahub"}
    headers = {
        "Accept": "application/json",
        "Prefer": "return=minimal",
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=myparams,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    if response.status_code == 404:
        return None

    response_json = json.loads(response.text)
    return response_json["ehr_id"]["value"]


def fetch_all_ehr_id() -> List[UUID]:
    """
    Returns a list of all ehr_id available on the EHRbase server

    Returns
    -------
    list[UUID]
        list of ehr_id available on the EHRbase server
    """
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = "SELECT e/ehr_id/value as ehr_id FROM EHR e"
    headers = {
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params={"q": query},
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    if response.ok:
        response_json = json.loads(response.text)
        return response_json["rows"]
    return []


def create_ehr(patient_id: str) -> UUID:
    """
    Check if patient_id is already registered, if so return existing ehr_id
    If the patient is new, register an ehr and return the ehr_id

    Parameters
    ----------
    patient_id: str
        External identifier for the patient

    Returns
    -------
    UUID
        ehr_id for the given patient id
    """
    ehr_id = get_ehr_id_for_patient_id(patient_id)
    if ehr_id:
        print(f"An EHR identifier already exists for this patient with UUID: {ehr_id}")
        return ehr_id

    url = f"{EHRBASE_BASE_URL}/ehr"
    id_payload = {
        "_type": "EHR_STATUS",
        "archetype_node_id": "openEHR-EHR-EHR_STATUS.generic.v1",
        "name": {"value": "EHR Status"},
        "subject": {
            "external_ref": {
                "id": {"_type": "GENERIC_ID", "value": patient_id, "scheme": "DataHub"},
                "namespace": "datahub",
                "type": "PERSON",
            }
        },
        "is_modifiable": True,
        "is_queryable": True,
    }

    headers = {"Accept": "application/json", "Prefer": "return=representation", "Content-Type": "application/json"}
    response = requests.request(
        "POST",
        url,
        data=json.dumps(id_payload),
        headers=headers,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    print(f"RESPONSE: {response.status_code}")
    response_json = json.loads(response.text)
    ehr_id = response_json["ehr_id"]["value"]
    print(f"EHR successfully created for this patient with UUID: {ehr_id}")
    return ehr_id
