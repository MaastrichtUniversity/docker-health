"""
Functions specific to the Patient template
"""
import sqlite3
from datetime import datetime
from typing import Optional
from xml.etree.ElementTree import Element

import pandas as pd
from pydantic import BaseModel, Field

from src.composition import datetime_now


class Patient(BaseModel):
    """Data model for the Patient class"""
    gender_code: str = Field(..., serialization_alias='sexAssignedAtBirth')
    birth_date: datetime = Field(..., serialization_alias='dateOfBirth')
    death_date: Optional[datetime] = Field(None, serialization_alias='dateOfDeath')
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias='startTime')


def create_patient_instance(gender_code, birth_date, death_date) -> Patient:
    """
    check ISO format and local terms of the parsed values and create a Patient attribute

    Parameters
    ----------
    gender_code: str
        The parsed gender code
    birth_date: str
        The parsed date of birth
    death_date: str
        The parsed date of death (optional)

    Returns
    -------
    Patient
        Instance of the Patient object
    """
    if gender_code not in ['M', 'F', 'I']:  # code for Male, Female, Intersec
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


def parse_patient_csv(patient_df: pd.DataFrame) -> (str, str, str):
    """
    Parse a csv file for a unique patient

    Parameters
    ----------
    patient_df: pd.DataFrame
        Dataframe that contains information on the patient

    Returns
    -------
    str
        The parsed gender code
    str
        The parsed date of birth
    str
        The parsed date of death (optional)
    """
    if len(patient_df) != 1:
        print("Need strictly one patient in the dataframe.")
        return 1
    patient_df = patient_df.squeeze()

    try:
        gender_code = patient_df['GENDER']
    except KeyError:
        gender_code = None

    try:
        birth_date = patient_df['BIRTHDATE']
    except KeyError:
        birth_date = None

    try:
        death_date = patient_df['DEATHDATE']
    except KeyError:
        death_date = None

    return gender_code, birth_date, death_date


def parse_patient_json(patient_json: dict) -> (str, str, str):
    """
    Parse a unique patient json file

    Parameters
    ----------
    patient_json: dict
        The json file that contains information on a patient, loaded as a python dict

    Returns
    -------
    str
        The parsed gender code
    str
        The parsed date of birth
    str
        The parsed date of death (optional)
    """
    try:
        gender_code = patient_json['attributes']['gender']
    except KeyError:
        gender_code = None

    try:
        birth_date = patient_json['attributes']['birthdate_as_localdate']
    except KeyError:
        birth_date = None

    try:
        death_date = patient_json['attributes']['deathdate']
    except KeyError:
        death_date = None

    return gender_code, birth_date, death_date


def parse_patient_ccda(patient_xml: Element) -> (str, str, str):
    """
    Parse a unique patient cdda xml file

    Parameters
    ----------
    patient_xml: Element
        root element of the patient xml.etree.ElementTree parsed file

    Returns
    -------
    str
        The parsed gender code
    str
        The parsed date of birth
    str
        The parsed date of death (optional)
    """
    try:
        gender_code = patient_xml.find(".//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}administrativeGenderCode").attrib['code']
    except KeyError:
        gender_code = None

    try:
        birth_date = patient_xml.find(".//{urn:hl7-org:v3}patient/{urn:hl7-org:v3}birthTime").attrib['value']
        birth_date = datetime.strptime(birth_date, '%Y%m%d%H%M%S')
        birth_date = datetime.isoformat(birth_date)
    except KeyError:
        birth_date = None

    # No real date of death, this is more a date of death certificate
    try:
        death_date = patient_xml.find(".//{urn:hl7-org:v3}code[@code='69409-1'].../{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}low").attrib['value']
        death_date = datetime.strptime(death_date, '%Y%m%d%H%M%S')
        death_date = datetime.isoformat(death_date)
    except KeyError:
        death_date = None
    except AttributeError:
        death_date = None

    return gender_code, birth_date, death_date


def parse_patient_sql(connection: sqlite3.Connection, patient_id: str) -> (str, str, str):
    """
    Parse a sql file for a unique patient

    Parameters
    ----------
    connection: sqlite3.connect
        Connection to sql data containing all patients
    patient_id: str
        External patient id

    Returns
    -------
    str
        The parsed gender code
    str
        The parsed date of birth
    str
        The parsed date of death (optional)
    """
    cursor = connection.cursor()
    try:
        select_query = "SELECT gender, birthdate, deathdate FROM Patients WHERE id = ?"
        cursor.execute(select_query, (patient_id,))
        result = cursor.fetchone()

        if result:
            gender, birthdate, deathdate = result
            return gender, birthdate, deathdate
        print(f"No record found with ID {patient_id}")
        return None

    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None

    finally:
        cursor.close()
