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


class Measure:
    def __init__(self, value, unit, unit_gt):
        try:
            self.value = float(value)
        except ValueError:
            self.value = None
        if unit != unit_gt:
            print("Wrong unit of measure: units is [{units}] but should be [{unit_gt}]!")
            self.unit = None
            self.value = None
        else:
            self.unit = str(unit)

class VitalSigns:
    """Data model for the vital signs"""
    def __init__(self, time, height, weight, heart_rate, blood_systolic, blood_diastolic):
        self.time = time # datetVITALSIGNS_VARIABLESime
        self.height = height # object instance
        self.weight = weight # object instance
        self.heart_rate = heart_rate # object instance
        self.blood_systolic = blood_systolic # object instance
        self.blood_diastolic = blood_diastolic # object instance

def parse_vitalsigns(vitalsigns_df: pd.DataFrame, vitalsigns_variables) -> VitalSigns:
    """
    Parse vital signs dataframe to a vital signs class
    Parameters
    ----------
    vitalsigns
        Pandas dataframe that contains the values for the vital signs

    Returns
    -------
    VitalSigns
        Instance of VitalSigns filled with the values

    """
    for variable in vitalsigns_variables:
        measurement = vitalsigns_df[vitalsigns_df["DESCRIPTION"] == variable["name"]].squeeze()
        time = measurement["DATE"]
        measure_instance = Measure(measurement["VALUE"], measurement["UNITS"], variable["units"])
        if variable["name"] == "Body Height":
            height = measure_instance
        elif variable["name"] == "Body Weight":
            weight = measure_instance 
        elif variable["name"] == "Heart rate":
            heart_rate = measure_instance 
        elif variable["name"] == "Systolic Blood Pressure":
            blood_systolic = measure_instance 
        elif variable["name"] == "Diastolic Blood Pressure":
            blood_diastolic = measure_instance
    return VitalSigns(time, height, weight, heart_rate, blood_systolic, blood_diastolic)

def update_composition_vitalsigns(composition: dict, vitalsigns: VitalSigns) -> dict:
    """
    Update the composition with the values from the vital signs dataframe
    Values:
        - Time of measurement
        - Body Height
        - Body Weight
        - Heart rate
        - Systolic Blood Pressure
        - Diastolic Blood Pressure

    Parameters
    ----------
    composition: dict
        The composition for which the values need to be updated
    vitalsigns: VitalSigns
        Contains all vital signs values

    Returns
    -------
    dict
        Updated composition
    """
    for archetype in composition["content"]:
        archetype["data"]["origin"]["value"] = vitalsigns.time
        archetype["data"]["events"][0]["time"]["value"] = vitalsigns.time
        if archetype["name"]["value"] == "Body Height":
            archetype["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = vitalsigns.height.value
        elif archetype["name"]["value"] == "Body weight":
            archetype["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = vitalsigns.weight.value
        elif archetype["name"]["value"] == "Heart rate":
            archetype["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = vitalsigns.heart_rate.value
        elif archetype["name"]["value"] == "Blood pressure":
            for item in archetype["data"]["events"][0]["data"]["items"]:
                if item["name"]["value"] == "Systolic":
                    item["value"]["magnitude"] = vitalsigns.blood_systolic.value
                elif item["name"]["value"] == "Diastolic":
                    item["value"]["magnitude"] = vitalsigns.blood_diastolic.value
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
