"""
Functions to transform and POST a composition to the EHRbase
"""

import json
import os
from datetime import datetime
from uuid import UUID
from pathlib import Path

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
        method="POST",
        url=url,
        headers=headers,
        data=simplified_composition,
        timeout=10,
    )
    composition = response.json()
    # print(json.dumps(composition, indent=4))
    return composition


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


def post_composition(ehr_id: UUID, composition: dict, write_composition: bool, json_filename: Path):
    """
    POST a composition to the EHRbase server

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given patient
    composition: dict
        Composition to be posted
    write_composition: bool
        if True, the composition is saved into a file
    json_filename: Path
        filename where the composition is saved
    """
    # print(json.dumps(composition))
    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition"
    headers = {
        "Accept": "application/json; charset=UTF-8",
        "Prefer": "return=representation",
        "Content-Type": "application/json",
    }
    response = requests.request(
        method="POST",
        url=url,
        headers=headers,
        data=json.dumps(composition),
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    response_json = json.loads(response.text)
    print(f"RESPONSE: {response.status_code}")
    if response.ok:
        print(f"Composition was successfully created with UUID: {response_json['uid']['value']}")
        if write_composition:
            write_json_composition(composition=composition, json_filename=json_filename)
    else:
        print(f"ERROR: {response_json['error']}")
        print(response_json["message"])


def update_composition(
    ehr_id: UUID, versioned_composition_id: UUID, new_composition: dict, write_composition: bool, json_filename: Path
):
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
    write_composition: bool
        if True, the composition is saved into a file
    json_filename: Path
        filename where the composition is saved
    """
    # print(json.dumps(composition))
    composition_uuid, _, version = versioned_composition_id.split("::")

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition/{composition_uuid}?openehrVersion={version}"
    headers = {
        "If-Match": versioned_composition_id,
        "Accept": "application/json; charset=UTF-8",
        "Prefer": "return=representation",
        "Content-Type": "application/json",
        "openEHR-AUDIT_DETAILS": "None",  # Not sure about the purpose of this header
    }
    response = requests.request(
        method="PUT",
        url=url,
        headers=headers,
        data=json.dumps(new_composition),
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    response_json = json.loads(response.text)
    print(f"RESPONSE: {response.status_code}")
    if response.ok:
        print(f"Composition was successfully updated with UUID: {response_json["uid"]["value"]}")
        if write_composition:
            write_json_composition(composition=new_composition, json_filename=json_filename)
    else:
        print(f"ERROR: {response_json['error']}")
        print(response_json["message"])


def delete_composition(ehr_id: UUID, versioned_composition_id: str):
    """
    DELETE a previously posted composition in the EHRbase server

    Parameters
    ----------
    ehr_id: UUID
        EHR uuid of a given patient
    versioned_composition_id: UUID
        Composition uuid in the format UUID::host::version.
    """
    # find the latest version
    latest_versioned_composition_id = get_all_versioned_composition_uuids(ehr_id, versioned_composition_id)[-1]

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition/{latest_versioned_composition_id}"
    headers = {
        "openEHR-AUDIT_DETAILS": "None",  # Not sure about the purpose of this header
    }
    response = requests.request(
        method="DELETE",
        url=url,
        headers=headers,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    # code error undocumented in EHRbase
    status_code = response.status_code
    print(f"RESPONSE: {status_code}")
    if status_code == 204:
        print("Composition was successfully deleted")
    elif status_code == 400:
        print("ERROR: Bad Request\nURL could not be parsed, or composition already deleted")
    elif status_code == 404:
        print("ERROR: Not Found\nehr_id and/or composition_id do not exist")
    elif status_code == 409:
        print("ERROR: Conflict\nversioned_composition_id does not match the latest version")


def get_all_versioned_composition_uuids(ehr_id: UUID, versioned_composition_id: str) -> list | None:
    """
    Retrieve all the versioned composition UUIDs in the format UUID::host::version.
    Ordered from the oldest to the latest version.

    Parameters
    ----------
    ehr_id: UUID
        EHR id of a given patient
    versioned_composition_id: UUID
        Base composition UUID without the host and version

    Returns
    -------
    list
        if response.ok is True:
        A list of versioned composition UUIDs in the format UUID::host::version,
        ordered from the oldest to the latest version.
    None
        if reponse.ok is False
    """
    base_composition_uuid, _, _ = versioned_composition_id.split("::")
    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/versioned_composition/{base_composition_uuid}/revision_history"
    headers = {
        "Accept": "application/json; charset=UTF-8",
    }
    response = requests.request(
        method="GET",
        url=url,
        headers=headers,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    response_json = json.loads(response.text)
    if response.ok:
        versioned_composition_uuids = []
        for item in response_json:
            versioned_composition_uuids.append(item["version_id"]["value"])
        return versioned_composition_uuids
    print(f"ERROR: {response_json['error']}")
    print(response_json["message"])
    return None


def get_composition_at_version(ehr_id: UUID, versioned_composition_id: str) -> str | None:
    """
    Get a composition at it's specific version.

    Parameters
    ----------
    versioned_composition_id: str
        Versioned composition UUID in the format UUID::host::version,
    ehr_id: UUID
        EHR id of a given patient

    Returns
    -------
    str
        The composition value as a string if response.ok is True
    None
        if response.ok is False
    """

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition/{versioned_composition_id}"
    headers = {
        "Accept": "application/json; charset=UTF-8",
    }
    response = requests.request(
        method="GET",
        url=url,
        headers=headers,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    # code error undocumented in EHRbase
    status_code = response.status_code
    print(f"RESPONSE: {status_code}")
    if status_code == 200:
        composition = response.json()
        return composition
    elif status_code == 204:
        print("ERROR: No Content\nThe composition has been deleted")
    elif status_code == 404:
        print("ERROR: Not Found\nehr_id and/or composition_id do not exist")
    return None
