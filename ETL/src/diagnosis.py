"""
Functions specific to the Diagnosis template
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional
from xml.etree.ElementTree import Element

import pandas as pd
from pydantic import BaseModel, Field, field_serializer

from src.composition import datetime_now

PLOT_PATH = Path("data/plot")


class Diagnosis(BaseModel):
    """Data model for the Diagnosis class"""

    snomed_code: int = Field(..., serialization_alias="diagnosisSNOMEDCode")
    description: str = Field(..., serialization_alias="diagnosisValue")
    start_date: datetime = Field(..., serialization_alias="dateOfDiagnosisValue")
    stop_date: Optional[datetime] = Field(None, serialization_alias="dateOfResolutionValue")
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias="startTime")

    @field_serializer("start_date")
    def serialize_start_date(self, dt: datetime, _info):
        return serialize_dt(dt)

    @field_serializer("stop_date")
    def serialize_stop_date(self, dt: datetime, _info):
        return serialize_dt(dt)


def serialize_dt(dt: datetime):
    dt_formatted = dt.strftime("%Y-%m-%dT%H:%M:%S")
    return dt_formatted


def create_diagnosis_instance(snomed_code: str, description: str, start_date: str, stop_date: str) -> Diagnosis:
    """
    check ISO format and local terms of the parsed values and create a Diagnosis attribute

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
    try:  # Do float SNOMED-ct codes exist?
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
            start_date=start_date,
        )

    return Diagnosis(
        snomed_code=snomed_code,
        description=description,
        start_date=start_date,
        stop_date=stop_date,
    )


def parse_all_diagnosis_csv(diagnosis_df: pd.DataFrame) -> (str, str, str, str):
    """
    Parse a csv file of a unique diagnosis

    Parameters
    ----------
    diagnosis_df: pd.DataFrame
        Dataframe that contains information on the diagnosis

    Returns
    -------
    str
        The parsed SNOMED-Ct code
    str
        The parsed description of the diagnosis
    str
        The parsed start date of the disorder/symptoms
    str
        The parsed end date of the disorder/symptoms (optional)
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


def parse_all_diagnosis_json(patient_json: dict, i: int, j: int) -> (str, str, str, str):
    """
    Parse a unique diagnosis json file

    Parameters
    ----------
    patient_json: dict
        The json file that contains information on a patient, loaded as a python dict
    i: int
        Increment to access a given encounter
    j: int
        Increment to access a given condition

    Returns
    -------
    str
        The parsed SNOMED-Ct code
    str
        The parsed description of the diagnosis
    str
        The parsed start date of the disorder/symptoms
    str
        The parsed end date of the disorder/symptoms (optional)
    """
    try:
        snomed_code = patient_json["record"]["encounters"][i]["conditions"][j]["codes"][0]["code"]
    except KeyError:
        snomed_code = None

    try:
        description = patient_json["record"]["encounters"][i]["conditions"][j]["codes"][0]["display"]
    except KeyError:
        description = None

    try:
        start_date = patient_json["record"]["encounters"][i]["conditions"][j]["start"]
        # convert sec to an actual date! Last 3 digits represents the time zone
        start_date_sec = int(str(start_date)[:-3])
        # tzinfo = int(str(start_date)[-3:]) # how to convert country integer code to letter code??
        start_date = datetime.fromtimestamp(start_date_sec)
        start_date = datetime.isoformat(start_date.astimezone())

    except KeyError:
        start_date = None

    try:
        stop_date = patient_json["record"]["encounters"][i]["conditions"][j]["stop"]
        # convert sec to an actual date! Last 3 digits represents the time zone
        stop_date_sec = int(str(stop_date)[:-3])
        # tzinfo = str(stop_date)[-3:] # how to convert country integer code to letter code??
        stop_date = datetime.fromtimestamp(stop_date_sec)
        stop_date = datetime.isoformat(stop_date.astimezone())
    except KeyError:
        stop_date = None
    except ValueError:
        stop_date = None
    return snomed_code, description, start_date, stop_date


def parse_all_diagnosis_ccda(entry_xml: Element) -> (str, str, str, str):
    """
    Parse a unique diagnosis ccda xml file

    Parameters
    ----------
    entry_xml: Element
        Part of the xml tree containing the diagnosis

    Returns
    -------
    str
        The parsed SNOMED-Ct code
    str
        The parsed description of the diagnosis
    str
        The parsed start date of the disorder/symptoms
    str
        The parsed end date of the disorder/symptoms (optional)
    """

    try:
        snomed_code = entry_xml.find(
            "./{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}value"
        ).attrib["code"]
    except KeyError:
        snomed_code = None
    except AttributeError:
        snomed_code = None

    try:
        description = entry_xml.find(
            "./{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}value"
        ).attrib["displayName"]
    except KeyError:
        description = None
    except AttributeError:
        description = None

    try:
        start_date = entry_xml.find(
            "./{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}low"
        ).attrib["value"]
        start_date = datetime.strptime(start_date, "%Y%m%d%H%M%S")
        start_date = datetime.isoformat(start_date.astimezone())
    except KeyError:
        start_date = None
    except AttributeError:
        start_date = None

    try:
        stop_date = entry_xml.find(
            "./{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}high"
        ).attrib["value"]
        stop_date = datetime.strptime(stop_date, "%Y%m%d%H%M%S")
        stop_date = datetime.isoformat(stop_date.astimezone())
    except KeyError:
        stop_date = None
    except AttributeError:
        stop_date = None

    return snomed_code, description, start_date, stop_date


def get_all_diagnosis_sql(connection: sqlite3.Connection, subject_id: str) -> list[dict]:
    """
    from the sql file, create a dictionary for each encountered disorder

    Parameters
    ----------
    conection:
        Connection to sql data containing all diagnosis
    subject_id: str
        External patient id

    Returns
    -------
    list[dict]
        List of dictionaries containing information for each disorder
    """
    cursor = connection.cursor()
    try:
        select_patient_disorders_query = "SELECT * FROM Conditions WHERE patient = ? AND description LIKE '%disorder%'"
        cursor.execute(select_patient_disorders_query, (subject_id,))
        result = cursor.fetchall()
        if result:
            # Convert each tuple in the result to a dictionary
            column_names = ["start_date", "stop_date", "patient_id", "encounter_id", "snomed_code", "description"]
            conditions = [dict(zip(column_names, row)) for row in result]
            return conditions
        print(f"No disorders found with ID {subject_id}")
        return None

    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None
    finally:
        cursor.close()


def parse_diagnosis_sql(diagnosis: dict) -> (str, str, str, str):
    """
    Parse a sql file of a unique diagnosis

    Parameters
    ----------
    diagnosis: list[dict]
        List of dictionaries containing information for each disorder

    Returns
    -------
    str
        The parsed SNOMED-Ct code
    str
        The parsed description of the diagnosis
    str
        The parsed start date of the disorder/symptoms
    str
        The parsed end date of the disorder/symptoms (optional)
    """
    try:
        snomed_code = diagnosis["snomed_code"]
    except KeyError:
        snomed_code = None

    try:
        description = diagnosis["description"]
    except KeyError:
        description = None

    try:
        start_date = diagnosis["start_date"]
    except KeyError:
        start_date = None

    try:
        stop_date = diagnosis["stop_date"]
    except KeyError:
        stop_date = None

    return snomed_code, description, start_date, stop_date


def parse_diagnosis_fhir(condition: dict) -> Diagnosis:
    """
    Parse a unique pre-filtered condition resource

    Parameters
    ----------
    condition: dict
        The pre-filtered condition resource

    Returns
    -------
    Diagnosis
        Instance of the Diagnosis object
    """
    try:
        for code in condition["code"]["coding"]:
            if "http://snomed.info/sct" in code["system"]:
                snomed_code = int(code["code"])
                description = code["display"]
                break
    except KeyError:
        snomed_code = None
        description = None

    try:
        start_date = condition["onsetDateTime"]
    except KeyError:
        start_date = None

    try:
        stop_date = condition["abatementDateTime"]
    except KeyError:
        stop_date = None
    except ValueError:
        stop_date = None

    return create_diagnosis_instance(snomed_code, description, start_date, stop_date)
