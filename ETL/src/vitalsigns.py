"""
Functions specific to the Vital Signs template
"""

import os
import json
from pathlib import Path
from datetime import datetime
from uuid import UUID
import requests
from pydantic import BaseModel, Field

import pandas as pd
import matplotlib.pyplot as plt

from src.composition import datetime_now

EHRBASE_USERRNAME = os.environ["EHRBASE_USERRNAME"]
EHRBASE_PASSWORD = os.environ["EHRBASE_PASSWORD"]
EHRBASE_BASE_URL = os.environ["EHRBASE_BASE_URL"]

PLOT_PATH = Path("data/plot")


class Measurement(BaseModel):
    """Data model for measurement"""

    value: float = Field(..., serialization_alias="magnitude")
    units: str = Field(..., serialization_alias="units")
    time: datetime = Field(None, serialization_alias="timeValue")


class PointsInTime(BaseModel):
    measurements: list[Measurement] = Field(..., serialization_alias="pointInTime")


class VitalSigns(BaseModel):
    """Data model for the vital signs"""

    height: PointsInTime = Field(..., serialization_alias="bodyHeightObservation")
    weight: PointsInTime = Field(..., serialization_alias="BodyWeightObservation")
    heart_rate: PointsInTime = Field(..., serialization_alias="HeartRateObservation")
    # blood_systolic: PointsInTime = Field(..., serialization_alias="BloodPressureObservation")
    # blood_diastolic: PointsInTime = Field(..., serialization_alias="BloodPressureObservation")
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias="startTime")


def parse_vital_signs_csv(vital_signs_df: pd.DataFrame) -> VitalSigns:
    """
    Parse vital signs dataframe to a vital signs class
    Parameters
    ----------
    vital_signs_df
        Pandas dataframe that contains the values for the vital signs for a single encounter

    Returns
    -------
    VitalSigns
        Instance of VitalSigns filled with the values

    """

    measurements = {}

    for _, vital_sign in vital_signs_df.iterrows():
        value = vital_sign["VALUE"]
        units = vital_sign["UNITS"]
        time = vital_sign["DATE"]
        if variable in measurements:
            measurements[vital_sign['DESCRIPTION']].append((value, units, time))
        else:
            measurements[vital_sign['DESCRIPTION']] = [(value, units, time)]

    return variable, value, unit, start_date


    #     if variable["name"] == "Body Height":
    #         measurements['height'].append(Measurement(value=value, units=units, time=time))
    #     if variable["name"] == "Body Weight":
    #         measurements['weight'].append(Measurement(value=value, units=units, time=time))
    #     if variable["name"] == "Heart rate":
    #         measurements['heart_rate'].append(Measurement(value=value, units=units, time=time))
    #     # if variable["name"] == "Systolic Blood Pressure":
    #     #     vital_signs.blood_systolic = measure_instance
    #     # if variable["name"] == "Diastolic Blood Pressure":
    #     #     vital_signs.blood_diastolic = measure_instance
    # height = PointsInTime(measurements=measurements['height'])
    # weight = PointsInTime(measurements=measurements['weight'])
    # heart_rate = PointsInTime(measurements=measurements['heart_rate'])

    return VitalSigns(height=height, weight=weight, heart_rate=heart_rate)


def parse_vital_signs_json(patient_json: dict, i: int, j: int):
    """
    TODO
    """
    try:
        variable = patient_json['record']['encounters'][i]['observations'][j]['codes'][0]['display']
    except KeyError:
        variable = None

    try:
        value = patient_json['record']['encounters'][i]['observations'][j]['value']
    except KeyError:
        value = None

    try:
        unit = patient_json['record']['encounters'][i]['observations'][j]['unit']
    except KeyError:
        unit = None

    try:
        start_date = patient_json['record']['encounters'][i]['observations'][j]['start']
        # convert sec to an actual date!
        # last 3 digits represent the time zone
        start_date_sec = int(str(start_date)[:-3])
        tzinfo = int(str(start_date)[-3:]) # how to convert country integer code to letter code??
        start_date = datetime.fromtimestamp(start_date_sec)
    except KeyError:
        start_date = None

    return variable, value, unit, start_date


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

    plt.savefig(PLOT_PATH / f"{ehr_id}_bloodpressure_over_time.png")
    plt.close()
