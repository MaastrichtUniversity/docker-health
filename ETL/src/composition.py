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

def load_composition_example(filename: str) -> dict:
    """
    Load an example composition and parse it to a python dictionary
    Parameters
    ----------
    filename: str
        Name of file which stores the composition

    Returns
    -------
    dict
        Parsed composition

    """
    with open(filename, "rb") as file:
        return json.load(file)

def dump_composition(composition: dict, filename: str):
    """
    Dump and save a composition as a JSON format.
    Parameters
    ----------
    composition: dict
        Composition stored as a python dictionary
    filename: str
        Name of file which stores the composition
    """
    with open(filename, "w") as file:
        json.dump(composition, file)

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
        print(f"Composition was successfully created")
        return response_json["uid"]["value"]
    else:
        print(f"ERROR {response_json["error"]}")
        print(response_json["message"])
        return None

def update_composition_high_level(composition: dict, start_time: datetime) -> dict:
    """
    Update the composition with:
        - territory
        - composer
        - encounter start time
        - encounter end time

    Parameters
    ----------
    composition: dict
        Composition that needs to be updated
    start_time: datetime
        Start time of the encounter
    end_time: datetime
        End ime of the encounter

    Returns
    -------
    dict
        Updated composition
    """
    # set territory
    composition["territory"]["code_string"] = "NL"
    # set composer
    composition["composer"]["name"] = "DataHub"
    # set start time
    composition["context"]["start_time"]["value"] = start_time
    # composition["context"]["end_time"] = {"value": end_time} # no end time
    return composition
