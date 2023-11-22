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


PLOT_PATH = Path("data/plot")


class Patient:
    """Data model for the Patient class"""
    def __init__(self, gender, birthdate, deathdate):
        self.gender = gender       # str
        self.birthdate = birthdate # datetime
        self.deathdate = deathdate # datetime

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
        deathdate = datetime.fromisoformat(patient_df["DEATHDATE"]).isoformat()
    except TypeError:
        deathdate = None

    return Patient(gender, birthdate, deathdate)

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
            archetype["data"]["items"][0]["value"]["value"] = patient.birthdate # patient.deathdate
    return composition
