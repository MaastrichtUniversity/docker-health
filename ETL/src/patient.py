"""
Functions specific to the Patient template
"""

import os
import json
from pathlib import Path
from datetime import datetime
from uuid import UUID
import requests
from pydantic import BaseModel

import pandas as pd


EHRBASE_USERRNAME = os.environ["EHRBASE_USERRNAME"]
EHRBASE_PASSWORD = os.environ["EHRBASE_PASSWORD"]
EHRBASE_BASE_URL = os.environ["EHRBASE_BASE_URL"]

PLOT_PATH = Path("data/plot")


class Patient(BaseModel):
    """Data model for the Patient class"""

    gender: str
    birthdate: datetime
    deathbirth: datetime

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

    patient = Patient

    # Parse Gender (Sex assigned at birth):
    gender = patient_df["GENDER"]
    if gender in ['M', 'F', 'I']: # code for Male, Female, Intersec
        patient.gender = gender
    else:
        patient.gender = None

    # Parse birthdate:
    birthdate = patient_df["BIRTHDATE"]
    try:
        date = datetime.fromisoformat(str(birthdate)) # str for None values
        patient.birthdate = date
    except ValueError:
        patient.birthdate = None

    # Parse deathdate:
    deathdate = patient_df["DEATHDATE"]
    try:
        date = datetime.fromisoformat(str(deathdate)) # str for None values
        patient.deathdate = date
    except ValueError:
        patient.deathdate = None

    return patient

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
    pass