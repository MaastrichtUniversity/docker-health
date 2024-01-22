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


def get_ehr_id_for_subject_id(subject_id: str) -> None | UUID:
    """
    Get the ehr_id for a patient given the subject external id

    Parameters
    ----------
    subject_id: str
        External subject id

    Returns
    -------
    UUID
        ehr_id if the patient already has an EHR (code error 404)
    None
        If the patient does not have an ehr
    """
    url = f"{EHRBASE_BASE_URL}/ehr"
    myparams = {"subject_id": subject_id, "subject_namespace": "datahub"}
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


def create_ehr(subject_id: str) -> UUID:
    """
    Check if subject_id is already registered, if so return existing ehr_id
    If the patient is new, register an ehr and return the ehr_id

    Parameters
    ----------
    subject_id: str
        External identifier for the subject

    Returns
    -------
    UUID
        ehr_id for the given subject id
    """
    ehr_id = get_ehr_id_for_subject_id(subject_id)
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
                "id": {"_type": "GENERIC_ID", "value": subject_id, "scheme": "DataHub"},
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


def get_ehr_summary(subject_id: UUID, subject_namespace: str) -> dict | None:
    """
    Get the EHR summary by the subject id. EHR summary contains information on
    the system_id, ehr_id, ehr_status and time_created.

    Parameters
    ----------
    subject_id: UUID
        External id of the given subject
    subject_namespace: str
        Namespace of the given subject

    Returns
    -------
    dict | None
        the EHR summary
    """
    url = f"{EHRBASE_BASE_URL}/ehr?subject_id={subject_id}&subject_namespace={subject_namespace}"

    headers = {"Accept": "application/json"}
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


def get_ehr_status(ehr_id: UUID) -> dict | None:
    """
    Retrieves the latest version the EHR_STATUS for a given ehr_id.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given subject

    Returns
    -------
    dict | None
        the EHR status or None if response.ok is False
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
    response_json = json.loads(response.text)
    if response.ok:
        return response_json

    print(f"ERROR: {response_json['error']}")
    print(response_json["message"])
    return None


def get_ehr_status_at_version(ehr_id: UUID, versioned_ehr_status_id: str) -> dict | None:
    """
    Retrieve the EHR status at a specific version for a given EHR.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given subject
    versioned_ehr_status_id: str
        Versioned EHR status UUID in the format UUID::host::version.

    Returns
    -------
    str or None
        If the response is successful, the ehr status as a string is returned.
        If the response is unsuccessful, None is returned.
    """
    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/ehr_status/{versioned_ehr_status_id}"
    headers = {"Accept": "application/json; charset=UTF-8"}
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


def update_ehr_status(ehr_id: UUID, versioned_ehr_status_id: str, new_ehr_status: dict):
    """
    Retrieves the EHR_STATUS associated with the given versioned ehr_id.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given subject
    versioned_ehr_status_id: str
        versioned EHR_STATUS id containing the UUID, host and version (UUID::host::version)
    new_ehr_status:
        Updated ehr status
    """
    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/ehr_status"

    headers = {
        "If-Match": versioned_ehr_status_id,
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

    response_json = json.loads(response.text)

    if response.ok:
        print(f"EHR status was successfully updated with UUID: {response_json["uid"]["value"]}")
    else:
        print(f"ERROR: {response_json['error']}")
        print(response_json["message"])


def update_ehr_is_modifiable(ehr_id: UUID, is_modifiable: bool):
    """
    Update the modifiability status of an EHR.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given subject
    is_modifiable: bool
        Flag to allowing or not the modifiability of the EHR
    """
    ehr_status = get_ehr_status(ehr_id)
    versioned_ehr_status_id = ehr_status["uid"]["value"]
    if ehr_status:
        ehr_status["is_modifiable"] = is_modifiable
        update_ehr_status(ehr_id, versioned_ehr_status_id, ehr_status)
        print(f"is_queryable set to {is_modifiable}")


def update_ehr_is_queryable(ehr_id: UUID, is_queryable: bool):
    """
    Update the queryability status of an EHR.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given subject
    is_queryable: bool
        Flag to allowing or not the modifiability of the EHR
    """
    ehr_status = get_ehr_status(ehr_id)
    versioned_ehr_status_id = ehr_status["uid"]["value"]
    if ehr_status:
        ehr_status["is_queryable"] = is_queryable
        update_ehr_status(ehr_id, versioned_ehr_status_id, ehr_status)
        print(f"is_queryable set to {is_queryable}")


def get_all_versioned_ehr_status_ids(ehr_id: UUID) -> list | None:
    """
    Retrieve all versioned EHR status UUIDs in the format UUID::host::version,
    ordered from the oldest to the latest version.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given subject

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
            versioned_ehr_status_uuids.append(item["version_id"]["value"])
        return versioned_ehr_status_uuids
    print(f"ERROR: {response_json['error']}")
    print(response_json["message"])
    return None
