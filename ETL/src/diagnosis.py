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


EHRBASE_USERRNAME = os.environ["EHRBASE_USERRNAME"]
EHRBASE_PASSWORD = os.environ["EHRBASE_PASSWORD"]
EHRBASE_BASE_URL = os.environ["EHRBASE_BASE_URL"]

PLOT_PATH = Path("data/plot")


class Diagnosis(BaseModel):
    """Data model for the diagnosis"""
    snomed_code: int
    description: str
    startdate: datetime
    stopdate: datetime

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
    diagnosis = Diagnosis

    # Parse SNOMED-CT CODE:
    snomed_code = diagnosis_df["CODE"]
    try:
        diagnosis.snomed_code = int(snomed_code)
    except ValueError:
        diagnosis.snomed_code = None

    # Parse description of the disorder:
    description = diagnosis_df["DESCRIPTION"]

    # Parse startdate (date of diagnosis):
    startdate = diagnosis_df["START"]
    try:
        date = datetime.fromisoformat(str(startdate)) # str for None values
        diagnosis.startdate = date
    except ValueError:
        diagnosis.startdate = None

    # Parse stopdate (date of reslution):
    stopdate = diagnosis_df["STOP"]
    try:
        date = datetime.fromisoformat(str(stopdate)) # str for None values
        diagnosis.stopdate = date
    except ValueError:
        diagnosis.stopdate = None

    return diagnosis

def update_composition_disgnosis(composition: dict, diagnosis: dict) -> dict:
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
    pass