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
        print("An EHR identifier already exists for this patient.")
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
    response_json = json.loads(response.text)

    return response_json["ehr_id"]["value"]


def get_ehr_status(ehr_id: UUID) -> dict:
    """
    Retrieves a version of the EHR_STATUS associated with the EHR identified by ehr_id.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given patient

    Returns
    -------
    dict
        ehr_status
    """

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/ehr_status"

    headers = {"Accept": "application/json"}
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    ehr_status = json.loads(response.text)
    if response.ok:
        return ehr_status

    print(f"ERROR: {ehr_status['error']}")
    print(ehr_status["message"])


def update_ehr_status(ehr_id: UUID, versioned_ehr_id: UUID, new_ehr_status: dict) -> dict:
    """
    Retrieves a version of the EHR_STATUS associated with the EHR identified by ehr_id.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given patient
    versioned_ehr_id
    new_ehr_status

    Returns
    -------
    dict
        ehr_status
    """

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/ehr_status"

    headers = {
        "If-Match": versioned_ehr_id,
        "Accept": "application/json; charset=UTF-8",
        "Prefer": "return=representation",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "PUT",
        url,
        headers=headers,
        data=json.dumps(new_ehr_status),
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    updated_ehr_status = json.loads(response.text)

    if response.ok:
        return updated_ehr_status

    print(f"ERROR: {updated_ehr_status['error']}")
    print(updated_ehr_status["message"])


def update_ehr_modifiability_status(ehr_id: UUID, is_modifiable: bool) -> UUID | None:
    """
    Update the modifiability status of an Electronic Health Record (EHR).

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given patient.
    is_modifiable: bool
        Flag to allow or disallow modifying the EHR.

    Returns
    -------
    UUID
        Updated EHR status uuid.
    None
        If something went wrong
    """
    ehr_status = get_ehr_status(ehr_id)

    if ehr_status:
        ehr_status["is_modifiable"] = is_modifiable
        posted_ehr_status = update_ehr_status(ehr_id, ehr_status["uid"]["value"], ehr_status)
        if posted_ehr_status:
            return posted_ehr_status["uid"]["value"]

    return None


def get_all_versioned_ehr_status_uuids(ehr_id: UUID) -> list | None:
    """
    Retrieve all versioned EHR status UUIDs in the format UUID::host::version,
    ordered from the oldest to the latest version.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given patient.

    Returns
    -------
    list or None
        If the response is successful, returns a list of versioned EHR status UUIDs
        If the response is unsuccessful, returns None.
    """

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/versioned_ehr_status/revision_history"
    headers = {
        "Accept": "application/json; charset=UTF-8",
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    response_json = json.loads(response.text)

    if response.ok:
        versioned_ehr_status_uuids = []
        for item in response_json:
            versioned_ehr_status_uuids.append(item['version_id']['value'])
        return versioned_ehr_status_uuids
    print(f"ERROR: {response_json['error']}")
    print(response_json["message"])
    return None


def get_ehr_status_at_version(ehr_id: UUID, versioned_ehr_status_id: UUID) -> dict | None:
    """
    Retrieve the EHR status at a specific version for a given EHR.

    Parameters
    ----------
    versioned_ehr_status_id: UUID
        Versioned EHR status UUID in the format UUID::host::version.
    ehr_id: UUID
        EHR id of a given patient.

    Returns
    -------
    str or None
        If the response is successful, the ehr status as a string is returned.
        If the response is unsuccessful, None is returned.
    """

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/ehr_status/{versioned_ehr_status_id}"
    headers = {
        "Accept": "application/json; charset=UTF-8",
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    response_json = json.loads(response.text)
    if response.ok:
        return response_json
    print(f"ERROR: {response_json['error']}")
    print(response_json["message"])
    return None
