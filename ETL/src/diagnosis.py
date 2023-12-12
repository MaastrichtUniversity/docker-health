"""
Functions specific to the Diagnosis template
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from pydantic import BaseModel, Field

from src.composition import datetime_now

PLOT_PATH = Path("data/plot")


class Diagnosis(BaseModel):
    """Data model for the diagnosis"""

    snomed_code: int = Field(..., serialization_alias="diagnosisSNOMEDCode")
    description: str = Field(..., serialization_alias="diagnosisValue")
    start_date: datetime = Field(..., serialization_alias="dateOfDiagnosisValue")
    stop_date: Optional[datetime] = Field(None, serialization_alias="dateOfResolutionValue")
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias="startTime")


def create_diagnosis_attribute(snomed_code, description, start_date, stop_date) -> Diagnosis:
    """
    check format (ISO and local terms) and create a Diagnosis attribute
    TO DO
    """
    try: # Do float SNOMED-ct codes exist?
        snomed_code = int(snomed_code)
    except ValueError and TypeError:
        snomed_code = None

    try:
        start_date = datetime.fromisoformat(start_date).isoformat()
    except TypeError:
        start_date = None

    try:
        stop_date = datetime.fromisoformat(stop_date).isoformat()
    except TypeError:
        stop_date = None

    if stop_date is None:
        return Diagnosis(snomed_code=snomed_code, description=description, start_date=start_date)

    return Diagnosis(snomed_code=snomed_code, description=description, start_date=start_date, stop_date=stop_date)


def parse_all_diagnosis_csv(diagnosis_df: pd.DataFrame):
    """
    TO DO
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
    try:
        snomed_code = diagnosis_df["CODE"]
    except KeyError:
        snomed_code = None

    try:
        description = diagnosis_df["DESCRIPTION"]
    except KeyError:
        description = None

    try:
        start_date = diagnosis_df["START"]
    except KeyError:
        start_date = None

    try:
        stop_date = diagnosis_df["STOP"]
    except KeyError:
        stop_date = None

    return snomed_code, description, start_date, stop_date


def parse_all_diagnosis_json(patient_json: dict, i: int, j: int):
    """
    TO DO
    """
    try:
        snomed_code = patient_json['record']['encounters'][i]['conditions'][j]['codes'][0]['code']
    except KeyError:
        snomed_code = None

    try:
        description = patient_json['record']['encounters'][i]['conditions'][j]['codes'][0]['display']
    except KeyError:
        description = None

    try:
        start_date = patient_json['record']['encounters'][i]['conditions'][j]['start']
        # convert sec to an actual date!
        # last 3 digits represent the time zone
        start_date_sec = int(str(start_date)[:-3])
        tzinfo = int(str(start_date)[-3:]) # how to convert country integer code to letter code??
        start_date = datetime.fromtimestamp(start_date_sec)
    except KeyError:
        start_date = None

    try:
        stop_date = patient_json['record']['encounters'][i]['conditions'][j]['stop']
        # convert sec to an actual date!
        # last 3 digits represent the time zone
        stop_date_sec = str(stop_date)[:-3]
        tzinfo = str(stop_date)[-3:] # how to convert country integer code to letter code??
        stop_date = datetime.fromtimestamp(stop_date_sec)
    except KeyError:
        stop_date = None

    return snomed_code, description, start_date, stop_date
