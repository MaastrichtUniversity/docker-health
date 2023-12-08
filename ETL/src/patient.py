"""
Functions specific to the Patient template
"""

from datetime import datetime
from typing import Optional

import pandas as pd
from pydantic import BaseModel, Field

from src.composition import datetime_now


class Patient(BaseModel):
    """Data model for the Patient class"""

    gender: str = Field(..., serialization_alias='sexAssignedAtBirth')
    birthdate: datetime = Field(..., serialization_alias='dateOfBirth')
    death_date: Optional[datetime] = Field(None, serialization_alias='dateOfDeath')
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias='startTime')


def parse_patient(patient_df: pd.DataFrame) -> Patient:
    """
    Parse a unique patient dataframe to a patient class
    Parameters
    ----------
    patient_df
        Pandas dataframe that contains information on the patient

    Returns
    -------
    Patient
        Instance of Patient filled with the values

    """
    if len(patient_df) != 1:
        print("Need strictly one patient.")
        return 1
    patient_df = patient_df.squeeze()

    # Parse Gender (Sex assigned at birth):
    gender = patient_df["GENDER"]
    if gender not in ['M', 'F', 'I']: # code for Male, Female, Intersec
        gender = None

    # Parse birthdate:
    try:
        birthdate = datetime.fromisoformat(patient_df["BIRTHDATE"]).isoformat()
    except TypeError:
        birthdate = None

    # Parse deathdate:
    try:
        death_date = datetime.fromisoformat(str(patient_df["DEATHDATE"]))  # str for None values
        return Patient(gender=gender, birthdate=birthdate, deathdate=death_date)
    except ValueError:
        return Patient(gender=gender, birthdate=birthdate)


def update_composition_patient(composition: dict, patient: Patient) -> dict:
    """
    Update the composition with the values from the patient dataframe
    Values:
        - Gender
        - Bithdate
        - Deathdate

    Parameters
    ----------
    composition: dict
        The composition for which the values need to be updated
    patient: Patient
        Contains all patient values

    Returns
    -------
    dict
        Updated composition
    """
    for archetype in composition["content"]:
        if archetype["name"]["value"] == "Gender":
            # archetype["data"]['items'][0]["value"]["value"] = patient.gender
            archetype["data"]['items'][0]["value"]["defining_code"]["code_string"] = patient.gender
            if patient.gender == "M":
                archetype["data"]['items'][0]["value"]["value"] = "Male"
            elif patient.gender == "F":
                archetype["data"]['items'][0]["value"]["value"] = "Female"
            elif patient.gender == "I":
                archetype["data"]['items'][0]["value"]["value"] = "Intersex"
        elif archetype["name"]["value"] == "Birth":
            # if patient.birthdate is None:
            #     archetype["data"]["items"][0]["value"] = ""
            # else:
            archetype["data"]["items"][0]["value"]["value"] = patient.birthdate
        elif archetype["name"]["value"] == "Death":
            # if patient.deathdate is None:
            #     archetype["data"]["items"][0]["value"] = ""
            # else:
            archetype["data"]["items"][0]["value"]["value"] = patient.birthdate  # patient.deathdate
    return composition
