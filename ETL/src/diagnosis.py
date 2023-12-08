"""
Functions specific to the Diagnosis template
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


class Diagnosis:
    """Data model for the diagnosis"""
    def __init__(self, snomed_code, description, startdate, stopdate):
        self.snomed_code = snomed_code # int
        self.description = description # str
        self.startdate = startdate     # datetime
        self.stopdate = stopdate       # datetime

def parse_all_diagnosis(diagnosis_df: pd.DataFrame) -> Diagnosis:
    """
    Parse the diagnosis dataframe (all diagnosis on a single patient) to disctionary of diagnosis class
    Parameters
    ----------
    all_diagnosis_df
        Pandas dataframe that contains the detailed of each diagnosis for a given patient

    Returns
    -------
    diagnosis_df
        Instance of Diagnosis filled with the values
    """
    # Parse SNOMED-CT CODE:
    snomed_code = diagnosis_df["CODE"]
    try:
        snomed_code = int(snomed_code)
    except ValueError:
        snomed_code = None

    # Parse description of the disorder:
    description = diagnosis_df["DESCRIPTION"]

    # Parse startdate (date of diagnosis):
    try:
        startdate = datetime.fromisoformat(diagnosis_df["START"]).isoformat()
    except TypeError:
        startdate = None

    # Parse stopdate (date of reslution):
    try:
        stopdate = datetime.fromisoformat(diagnosis_df["STOP"]).isoformat()
    except TypeError:
        stopdate = None

    return Diagnosis(snomed_code, description, startdate, stopdate)

def update_composition_diagnosis(composition: dict, diagnosis: Diagnosis) -> dict:
    """
    Update the composition with the values from the diagnosis dataframe
    Values:
        - CNOMED-CT code
        - Description of the disorder
        - Date of the diagnosis
        - Date of resolution

    Parameters
    ----------
    composition: dict
        The composition for which the values need to be updated
    all_diagnosis: Diagnosis
        Contains all diagnosis values

    Returns
    -------
    dict
        Updated composition
    """
    for archetype in composition["content"]:
        if archetype["name"]["value"] == "Diagnosis":
            for item in archetype["data"]['items']:
                if item["name"]["value"] == "Diagnosis":
                    item["value"]["value"] = diagnosis.description
                    item["value"]["defining_code"]["code_string"] = str(diagnosis.snomed_code)
                    item["value"]["defining_code"]["terminology_id"]["value"] = "SNOMED-CT"
                elif item["name"]["value"] == "Date of Diagnosis":
                    item["value"]["value"] = diagnosis.startdate
                elif item["name"]["value"] == "Date of Resolution":
                    item["value"]["value"] = diagnosis.stopdate
    return composition
