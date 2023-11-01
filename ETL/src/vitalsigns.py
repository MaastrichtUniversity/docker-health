"""
Functions specific to the Vital Signs template
"""

import os
import json
from pathlib import Path
from datetime import datetime
from uuid import UUID
import requests
from pydantic import BaseModel

import pandas as pd
import matplotlib.pyplot as plt


EHRBASE_USERRNAME = os.environ["EHRBASE_USERRNAME"]
EHRBASE_PASSWORD = os.environ["EHRBASE_PASSWORD"]
EHRBASE_BASE_URL = os.environ["EHRBASE_BASE_URL"]

PLOT_PATH = Path("data/plot")


class VitalSigns(BaseModel):
    """Data model for the vital signs"""

    systolic: float
    diastolic: float
    time: datetime
    bmi: float
    height: float
    weight: float
    heart_rate: float
    respiration_rate: float

def parse_vital_signs(vital_signs: pd.DataFrame) -> VitalSigns:
    """
    Parse vital signs dataframe to a vital signs class
    Parameters
    ----------
    vital_signs
        Pandas dataframe that contains the values for the vital signs

    Returns
    -------
    VitalSigns
        Instance of VitalSigns filled with the values

    """
    results = VitalSigns
    results.systolic = vital_signs[vital_signs["DESCRIPTION"] == "Systolic Blood Pressure"]["VALUE"].values[0]
    results.diastolic = vital_signs[vital_signs["DESCRIPTION"] == "Diastolic Blood Pressure"]["VALUE"].values[0]
    results.time = vital_signs[vital_signs["DESCRIPTION"] == "Systolic Blood Pressure"]["DATE"].values[0]
    results.bmi = vital_signs[vital_signs["DESCRIPTION"] == "Body mass index (BMI) [Ratio]"]["VALUE"].values[0]
    results.height = vital_signs[vital_signs["DESCRIPTION"] == "Body Height"]["VALUE"].values[0]
    results.weight = vital_signs[vital_signs["DESCRIPTION"] == "Body Weight"]["VALUE"].values[0]
    results.heart_rate = vital_signs[vital_signs["DESCRIPTION"] == "Heart rate"]["VALUE"].values[0]
    results.respiration_rate = vital_signs[vital_signs["DESCRIPTION"] == "Respiratory rate"]["VALUE"].values[0]
    return results

def update_composition_vital_signs(composition: dict, vital_signs: VitalSigns) -> dict:
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
    vital_signs: VitalSigns
        Contains all vital signs values

    Returns
    -------
    dict
        Updated composition
    """

    for index, item in enumerate(composition["content"]):
        # Update bloodpressure
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.blood_pressure.v2":
            composition["content"][index]["data"]["origin"]["value"] = vital_signs.time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = vital_signs.time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"][
                "magnitude"
            ] = vital_signs.systolic
            composition["content"][index]["data"]["events"][0]["data"]["items"][1]["value"][
                "magnitude"
            ] = vital_signs.diastolic
        # update BMI
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.body_mass_index.v2":
            composition["content"][index]["data"]["origin"]["value"] = vital_signs.time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = vital_signs.time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"][
                "magnitude"
            ] = vital_signs.bmi
        # Update height
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.height.v2":
            composition["content"][index]["data"]["origin"]["value"] = vital_signs.time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = vital_signs.time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"][
                "magnitude"
            ] = vital_signs.height
        # Update weight
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.body_weight.v2":
            composition["content"][index]["data"]["origin"]["value"] = vital_signs.time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = vital_signs.time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"][
                "magnitude"
            ] = vital_signs.weight

        # Update heart rate
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.pulse.v2":
            composition["content"][index]["data"]["origin"]["value"] = vital_signs.time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = vital_signs.time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"][
                "magnitude"
            ] = vital_signs.heart_rate

        # Update respiration rate
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.respiration.v2":
            composition["content"][index]["data"]["origin"]["value"] = vital_signs.time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = vital_signs.time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"][
                "magnitude"
            ] = vital_signs.respiration_rate

    return composition

def remove_pulse_oximetry_from_composition(composition: dict) -> dict:
    """
    Remove pulse oximetry observation from composition
    Parameters
    ----------
    composition: dict
        The composition for which the values need to be removed

    Returns
    -------
    dict
        Updated composition
    """
    for index, item in enumerate(composition["content"]):
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.pulse_oximetry.v1":
            del composition["content"][index]
    return composition

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
        "GET", url, headers=headers, params={"q": query},
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD), timeout=10
    )
    response_json = json.loads(response.text)
    dataframe = pd.DataFrame(columns=["Time", "Systolic", "Diastolic"])

    for row in response_json["rows"]:
        dataframe.loc[len(dataframe)] = [row[0]["value"], row[1], row[2]]

    dataframe["Time"] = pd.to_datetime(dataframe["Time"])
    dataframe = dataframe.sort_values(by="Time")
    dataframe.set_index("Time", inplace=True)
    dataframe.plot()

    plt.savefig(PLOT_PATH / f"{ehr_id}_bloodpressure_over_time.png")
    plt.close()
