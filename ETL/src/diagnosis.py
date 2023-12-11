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

    snomed_code: str = Field(..., serialization_alias="diagnosisSNOMEDCode")
    description: str = Field(..., serialization_alias="diagnosisValue")
    startdate: datetime = Field(..., serialization_alias="dateOfDiagnosisValue")
    stopdate: Optional[datetime] = Field(None, serialization_alias="dateOfResolutionValue")
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias="startTime")


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
        snomed_code = str(snomed_code)
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
        return Diagnosis(snomed_code=snomed_code, description=description, startdate=startdate)

    return Diagnosis(snomed_code=snomed_code, description=description, startdate=startdate, stopdate=stopdate)
