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

    gender_code: str = Field(..., serialization_alias="sexAssignedAtBirth")
    birth_date: datetime = Field(..., serialization_alias="dateOfBirth")
    death_date: Optional[datetime] = Field(None, serialization_alias="dateOfDeath")
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias="startTime")


def create_patient_attribute(gender_code, birth_date, death_date) -> Patient:
    """
    check format (ISO and local terms) and create a Patient attribute
    TO DO
    """
    if gender_code not in ["M", "F", "I"]:  # code for Male, Female, Intersec
        gender_code = None

    try:
        birth_date = datetime.fromisoformat(birth_date)
    except TypeError:
        birth_date = None

    try:
        death_date = datetime.fromisoformat(death_date)
    except TypeError:
        death_date = None

    if death_date is None:
        return Patient(gender_code=gender_code, birth_date=birth_date)

    return Patient(gender_code=gender_code, birth_date=birth_date, death_date=death_date)


def parse_patient_csv(patient_df: pd.DataFrame):
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
        print("Need strictly one patient in the dataframe.")
        return 1
    patient_df = patient_df.squeeze()

    try:
        gender_code = patient_df["GENDER"]
    except KeyError:
        gender_code = None

    try:
        birth_date = patient_df["BIRTHDATE"]
    except KeyError:
        birth_date = None

    try:
        death_date = patient_df["DEATHDATE"]
    except KeyError:
        death_date = None

    return gender_code, birth_date, death_date


def parse_patient_json(patient_json: dict):
    """
    TO DO
    """
    try:
        gender_code = patient_json["attributes"]["gender"]
    except KeyError:
        gender_code = None

    try:
        birth_date = patient_json["attributes"]["birthdate_as_localdate"]
    except KeyError:
        birth_date = None

    try:
        death_date = patient_json["attributes"]["deathdate"]
    except KeyError:
        death_date = None

    return gender_code, birth_date, death_date
