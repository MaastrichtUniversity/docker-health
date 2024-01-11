"""
Functions to transform and POST a composition to the EHRbase
"""

import json
import os
from datetime import datetime
from uuid import UUID

import pytz
import requests

NLTZ = pytz.timezone("Europe/Amsterdam")
EHRBASE_USERRNAME = os.environ["EHRBASE_USERRNAME"]
EHRBASE_PASSWORD = os.environ["EHRBASE_PASSWORD"]
EHRBASE_BASE_URL = os.environ["EHRBASE_BASE_URL"]


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
        "accept": "*/*",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "POST",
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
        if response.ok is True:
        Versioned id of the composition, containing the host and version (UUID::host::version)
    None
        if reponse.ok is False
    """
    # print(json.dumps(composition))
    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition"
    headers = {
        "Accept": "application/json; charset=UTF-8",
        "Prefer": "return=representation",
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
        print("Composition was successfully created")
        return response_json["uid"]["value"]
    print(f"ERROR {response_json['error']}")
    print(response_json["message"])
    return None


def update_composition(ehr_id: UUID, versioned_composition_id: UUID, new_composition: dict) -> UUID | None:
    """
    PUT (update) a previously posted composition in the EHRbase server

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given patient
    versioned_composition_id: UUID
        Composition UUID, containing the host and version (UUID::host::version)
    new_composition: dict
        Updated composition

    Returns
    -------
    UUID
        versioned id of the composition, if response.ok is True
    None
        if reponse.ok is False
    """
    # print(json.dumps(composition))
    composition_uuid, host, version = versioned_composition_id.split("::")

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition/{composition_uuid}?openehrVersion={version}"
    headers = {
        "If-Match": versioned_composition_id,
        "Accept": "application/json; charset=UTF-8",
        "Prefer": "return=representation",
        "Content-Type": "application/json",
        "openEHR-AUDIT_DETAILS": "None", # Not sure about the purpose of this header
    }
    response = requests.request(
        "PUT",
        url,
        headers=headers,
        data=json.dumps(new_composition),
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    response_json = json.loads(response.text)
    print(f"RESPONSE: {response.status_code}")
    if response.ok:
        print("Update composition was successfully created")
        return response_json["uid"]["value"]
    print(f"ERROR {response_json['error']}")
    print(response_json["message"])
    return None


def delete_composition(ehr_id: UUID, versioned_composition_id: UUID) -> UUID | None:
    """
    DELETE a previously posted composition in the EHRbase server

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given patient
    versioned_composition_id: UUID
        Composition UUID, containing the host and version (UUID::host::version)
        Must be the last version
    """
    # print(json.dumps(composition))
    composition_uuid, host, version = versioned_composition_id.split("::")
        # check if this is the lastest version !

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition/{versioned_composition_id}"
    headers = {
        "openEHR-AUDIT_DETAILS": "None", # Not sure about the purpose of this header
    }
    response = requests.request(
        "DELETE",
        url,
        headers=headers,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    print(response)

    # Script below cannot work since the status codes are undocumented /!\
    # response_json = json.loads(response.text)
    # print(f"RESPONSE: {response.status_code}")
    # if response.ok:
    #     print("Composition was successfully deleted")
    # print(f"ERROR {response_json['error']}")
    # print(response_json["message"])


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
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(composition, file, indent=4)
