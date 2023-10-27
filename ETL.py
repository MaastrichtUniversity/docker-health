import json
from datetime import datetime
from typing import List
from uuid import UUID

import requests
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

EHRBASE_USERRNAME = "ehrbase-user"
EHRBASE_PASSWORD = "SuperSecretPassword"
EHRBASE_BASE_URL = "http://localhost:8080/ehrbase/rest/openehr/v1"


def list_all_templates() -> None:
    """
    Print all template available on the server
    """
    url = f"{EHRBASE_BASE_URL}/definition/template/adl1.4"

    headers = {
        "Accept": "application/json",
        "Prefer": "return=minimal",
    }

    response = requests.request("GET", url, headers=headers, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD), timeout=10)
    if response.ok:
        response_json = json.loads(response.text)
        for template in response_json:
            print(
                f"{template['concept']}\t{template['template_id']}\t{template['archetype_id']}\t{template['created_timestamp']}"
            )


def get_all_ehr_id() -> List[UUID]:
    """
    Returns a list of all ehr_id available on the server

    Returns
    -------
    list[UUID]
        list of ehr_id available on the server
    """
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = "SELECT e/ehr_id/value as ehr_id FROM EHR e"
    headers = {
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.request(
        "GET", url, headers=headers, params={"q": query}, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD), timeout=10
    )
    if response.ok:
        response_json = json.loads(response.text)
        return response_json["rows"]
    return []


def plot_bloodpressure_over_time(ehr_id: UUID) -> None:
    """
    Plot and save a graph of systolic and diastolic bloodpressure for a given patient using the vital signs template

    Parameters
    ----------
    ehr_id: UUID
        ehr_id of the patient for which the data will be plotted

    """
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = f"SELECT c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/time as time,  c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0004]/value/magnitude as systolic ,  c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0005]/value/magnitude as diastolic FROM EHR e CONTAINS COMPOSITION c WHERE c/archetype_details/template_id/value='Vital signs' AND e/ehr_id/value='{ehr_id}'"
    headers = {
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.request(
        "GET", url, headers=headers, params={"q": query}, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD), timeout=10
    )
    response_json = json.loads(response.text)
    dataframe = pd.DataFrame(columns=["Time", "Systolic", "Diastolic"])

    for row in response_json["rows"]:
        dataframe.loc[len(dataframe)] = [row[0]["value"], row[1], row[2]]

    dataframe["Time"] = pd.to_datetime(dataframe["Time"])
    dataframe = dataframe.sort_values(by="Time")
    dataframe.set_index("Time", inplace=True)
    dataframe.plot()
    plt.savefig(f"{ehr_id}_bloodpressure_over_time.png")
    plt.show()


def post_template(filename: str) -> None:
    """
    Post a template to the server. The template is provided as a filename which will be loaded
    Parameters
    ----------
    filename: str
        Name of the template that be loaded  from disk
    """
    url = f"{EHRBASE_BASE_URL}/definition/template/adl1.4"

    payload = open(filename, "rb").read()

    headers = {"Accept": "application/xml", "Prefer": "return=minimal", "Content-Type": "application/xml"}

    response = requests.request(
        "POST", url, headers=headers, data=payload, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD), timeout=10
    )

    if response.ok:
        print(f"Template {filename} successfully added")


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
    ehr_id = get_ehr_id_for_subject_id(patient_id)
    if ehr_id:
        return ehr_id

    url = f"{EHRBASE_BASE_URL}/ehr"
    id_payload = {
        "_type": "EHR_STATUS",
        "archetype_node_id": "openEHR-EHR-EHR_STATUS.generic.v1",
        "name": {"value": "EHR Status"},
        "subject": {
            "external_ref": {
                "id": {"_type": "GENERIC_ID", "value": patient_id, "scheme": "datahub"},
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


def get_ehr_id_for_subject_id(subject_id: str) -> None | UUID:
    """
    Get the ehr_id for a patient given the patient external id.
    Return nothing if the patient is unknow
    Parameters
    ----------
    subject_id: str
        patient external id

    Returns
    -------
    UUID
        ehr_id if the patient already has an ehr
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
        "GET", url, headers=headers, params=myparams, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD), timeout=10
    )

    if response.status_code == 404:
        return None

    response_json = json.loads(response.text)
    return response_json["ehr_id"]["value"]


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
    file = open(filename, "rb")
    return json.load(file)


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

    return response_json["uid"]["value"]


def update_composition_high_level(composition: dict, start_time: datetime, end_time: datetime) -> dict:
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
    composition["context"]["end_time"] = {"value": end_time}
    return composition


def update_composition_vital_signs(composition: dict, vital_signs: DataFrame) -> dict:
    """
    Update the composition with the values from the vital signs dataframe
    Values:
        - Systolic Blood Pressure
        - Diastolic Blood Pressure
        - Time of measurement
        - Body mass index
        - Body Height
        - Body Weight
        - Heart rate
        - Respiratory rate

    Parameters
    ----------
    composition: dict
        The composition for which the values need to be updated
    vital_signs: DataFrame
        Pandas dataframe that contains the values for the vital signs

    Returns
    -------
    dict
        Updated composition
    """
    systolic = vital_signs[vital_signs["DESCRIPTION"] == "Systolic Blood Pressure"]["VALUE"].values[0]
    diastolic = vital_signs[vital_signs["DESCRIPTION"] == "Diastolic Blood Pressure"]["VALUE"].values[0]
    time = vital_signs[vital_signs["DESCRIPTION"] == "Systolic Blood Pressure"]["DATE"].values[0]
    bmi = vital_signs[vital_signs["DESCRIPTION"] == "Body mass index (BMI) [Ratio]"]["VALUE"].values[0]
    height = vital_signs[vital_signs["DESCRIPTION"] == "Body Height"]["VALUE"].values[0]
    weight = vital_signs[vital_signs["DESCRIPTION"] == "Body Weight"]["VALUE"].values[0]
    heart_rate = vital_signs[vital_signs["DESCRIPTION"] == "Heart rate"]["VALUE"].values[0]
    respiration_rate = vital_signs[vital_signs["DESCRIPTION"] == "Respiratory rate"]["VALUE"].values[0]

    for index, item in enumerate(composition["content"]):
        # Update bloodpressure
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.blood_pressure.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = systolic
            composition["content"][index]["data"]["events"][0]["data"]["items"][1]["value"]["magnitude"] = diastolic
        # update BMI
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.body_mass_index.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = bmi
        # Update height
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.height.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = height
        # Update weight
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.body_weight.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = weight

        # Update heart rate
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.pulse.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = heart_rate

        # Update respiration rate
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.respiration.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"][
                "magnitude"
            ] = respiration_rate

    return composition


def main():
    """
    Post template
    Post vital sign compositions for a patient
    """
    # all_ehr_ids = get_all_ehr_id()
    # list_all_templates()
    post_template("vital_signs.opt")
    # list_all_templates()

    patient_id = "a2f7ab19-64e1-6fb3-7232-413f04c55100"

    ehr_id = create_ehr(patient_id)

    observations = pd.read_csv("synthea_csv/observations.csv")
    encounters = pd.read_csv("synthea_csv/encounters.csv")

    patient_encounters = encounters.loc[encounters["PATIENT"] == patient_id]
    encounter_ids = patient_encounters["Id"].tolist()

    for encounter_id in encounter_ids:
        composition = load_composition_example("vital_signs_20231025075308_000001_1.json")

        encounter_start = encounters.loc[encounters["Id"] == encounter_id]["START"].values[0]
        encounter_stop = encounters.loc[encounters["Id"] == encounter_id]["STOP"].values[0]

        composition = update_composition_high_level(composition, encounter_start, encounter_stop)

        if observations.loc[observations["ENCOUNTER"] == encounter_id].shape[0] == 0:
            print(f"{encounter_id} has no observations")
            continue

        vital_signs = observations[
            (observations["ENCOUNTER"] == encounter_id) & (observations["CATEGORY"] == "vital-signs")
        ]
        if vital_signs.shape[0] == 0:
            print(f"{encounter_id} has no vital signs observations")
            continue

        composition = update_composition_vital_signs(composition, vital_signs)
        post_composition(ehr_id, composition)

    plot_bloodpressure_over_time(ehr_id)


if __name__ == "__main__":
    main()
