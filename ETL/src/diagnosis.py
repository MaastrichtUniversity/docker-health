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
    """Data model for the Diagnosis class"""
    snomed_code: int = Field(..., serialization_alias='diagnosisSNOMEDCode')
    description: str = Field(..., serialization_alias='diagnosisValue')
    start_date: datetime = Field(..., serialization_alias='dateOfDiagnosisValue')
    stop_date: Optional[datetime] = Field(None, serialization_alias='dateOfResolutionValue')
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias='startTime')


def create_diagnosis_instance(snomed_code, description, start_date, stop_date) -> Diagnosis:
    """check ISO format and local terms of the parsed values and create a Diagnosis attribute

    Parameters
    ----------
    snomed_code: str
        The parsed SNOMED-Ct code 
    description: str
        The parsed description of the diagnosis
    start_date: str
        The parsed start date of the disorder/symptoms
    stop_date: str
        The parsed end date of the disorder/symptoms (optional)

    Returns
    -------
    Diagnosis
        Instance of the Diagnosis object
    """
    try: # Do float SNOMED-ct codes exist?
        snomed_code = int(snomed_code)
    except (ValueError, TypeError):
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
        return Diagnosis(
            snomed_code=snomed_code,
            description=description,
            start_date=start_date
        )

    return Diagnosis(
        snomed_code=snomed_code,
        description=description,
        start_date=start_date,
        stop_date=stop_date
    )


def parse_all_diagnosis_csv(diagnosis_df: pd.DataFrame):
    """Parse a csv file of a unique diagnosis

    Parameters
    ----------
    diagnosis_df: pd.DataFrame
        Dataframe that contains information on the diagnosis


    Returns
    -------
    snomed_code: str
        The parsed SNOMED-Ct code 
    description: str
        The parsed description of the diagnosis
    start_date: str
        The parsed start date of the disorder/symptoms
    stop_date: str
        The parsed end date of the disorder/symptoms (optional)
    """
    try:
        snomed_code = diagnosis_df['CODE']
    except KeyError:
        snomed_code = None

    try:
        description = diagnosis_df['DESCRIPTION']
    except KeyError:
        description = None

    try:
        start_date = diagnosis_df['START']
    except KeyError:
        start_date = None

    try:
        stop_date = diagnosis_df['STOP']
    except KeyError:
        stop_date = None

    return snomed_code, description, start_date, stop_date


def parse_all_diagnosis_json(patient_json: dict, i: int, j: int):
    """Parse a unique diagnosis json file

    Parameters
    ----------
    patient_json: dict
        The json file that containes information on a diagnosis, loaded as a python dict

    Returns
    -------
    snomed_code: str
        The parsed SNOMED-Ct code 
    description: str
        The parsed description of the diagnosis
    start_date: str
        The parsed start date of the disorder/symptoms
    stop_date: str
        The parsed end date of the disorder/symptoms (optional)
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
        # convert sec to an actual date! Last 3 digits represents the time zone
        start_date_sec = int(str(start_date)[:-3])
        # tzinfo = int(str(start_date)[-3:]) # how to convert country integer code to letter code??
        start_date = str(datetime.fromtimestamp(start_date_sec))
    except KeyError:
        start_date = None

    try:
        stop_date = patient_json['record']['encounters'][i]['conditions'][j]['stop']
        # convert sec to an actual date! Last 3 digits represents the time zone
        stop_date_sec = int(str(stop_date)[:-3])
        # tzinfo = str(stop_date)[-3:] # how to convert country integer code to letter code??
        stop_date = str(datetime.fromtimestamp(stop_date_sec))
    except KeyError:
        stop_date = None

    return snomed_code, description, start_date, stop_date
