"""
Functions specific to the Vital Signs template
"""
import sqlite3
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import pandas as pd

from src.composition import datetime_now


class Measurement(BaseModel):
    """Data model for the Measurement class"""

    value: float = Field(..., serialization_alias="magnitude")
    units: str = Field(..., serialization_alias="units")
    time: datetime = Field(None, serialization_alias="timeValue")


class PointsInTime(BaseModel):
    """Data model for the PointsInTime class"""

    measurements: list[Measurement] = Field(..., serialization_alias="pointInTime")


class VitalSigns(BaseModel):
    """Data model for the VitalSigns class"""

    height: Optional[PointsInTime] = Field(None, serialization_alias="bodyHeightObservation")
    weight: Optional[PointsInTime] = Field(None, serialization_alias="bodyWeightObservation")
    heart_rate: Optional[PointsInTime] = Field(None, serialization_alias="heartRateObservation")
    blood_systolic: Optional[PointsInTime] = Field(None, serialization_alias="bloodPressureSystolicObservation")
    blood_diastolic: Optional[PointsInTime] = Field(None, serialization_alias="bloodPressureDiastolicObservation")
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias="startTime")


def create_vital_signs_instance(all_vital_signs_measures: list, vital_signs_units: dict) -> VitalSigns:
    """
    check ISO format and local terms of the parsed values and create a VitalSigns attribute

    Parameters
    ----------
    all_vital_signs_measures: list
        List containing all the parsed values, stored as a dictionary for each measurement.
        {variable: str, value: str, unit: str, time: str}
    vital_signs_units: dict
        Dictionary describing the chosen units for each measurement

    Returns
    -------
    VitalSigns
        Instance of the VitalSigns object
    """
    grouped_measures = {}

    for measure in all_vital_signs_measures:
        variable_name = measure["variable_name"]

        if variable_name not in vital_signs_units.keys():
            # Keep only defined vital signs:
            continue
        try:
            value = float(measure["value"])
        except (ValueError, TypeError):
            value = None

        try:
            time = datetime.fromisoformat(measure["time"]).isoformat()
        except TypeError:
            time = None

        if measure["units"] != vital_signs_units[variable_name]:
            print("Units of measurement is inconsistent.", end=" ")
            print(f"Units is in {measure['units']} but should be in {vital_signs_units[value]}.")
            units = None
            value = None
            time = None

        else:
            units = str(measure["units"])

        if variable_name not in grouped_measures:
            grouped_measures[variable_name] = []
        grouped_measures[variable_name].append(Measurement(value=value, units=units, time=time))

    grouped_measures_pointintime = {}
    for var in vital_signs_units.keys():
        try:
            grouped_measures_pointintime[var] = PointsInTime(measurements=grouped_measures[var])
        except KeyError:
            grouped_measures_pointintime[var] = None

    return VitalSigns(
        height=grouped_measures_pointintime["Body Height"],
        weight=grouped_measures_pointintime["Body Weight"],
        heart_rate=grouped_measures_pointintime["Heart rate"],
        blood_systolic=grouped_measures_pointintime["Systolic Blood Pressure"],
        blood_diastolic=grouped_measures_pointintime["Diastolic Blood Pressure"],
    )


def parse_vital_signs_csv(vital_signs_enc_df: pd.DataFrame) -> list:
    """
    Parse a csv file of all vital signs measurements

    Parameters
    ----------
    vital_signs_enc_df
        Dataframe that contains information on multiple vital signs measurements
        within the same encounter

    Returns
    -------
    list
        List containing all the parsed values, stored as a dictionary for each measurement.
        {variable: str, value: str, unit: str, time: str}
    """
    all_vital_signs_measures = []
    for _, vital_sign in vital_signs_enc_df.iterrows():
        try:
            variable = vital_sign["DESCRIPTION"]
        except KeyError:
            variable = None

        try:
            value = vital_sign["VALUE"]
        except KeyError:
            value = None

        try:
            units = vital_sign["UNITS"]
        except KeyError:
            units = None

        try:
            time = vital_sign["DATE"]
        except KeyError:
            time = None

        all_vital_signs_measures.append({"variable_name": variable, "value": value, "units": units, "time": time})

    return all_vital_signs_measures


def parse_vital_signs_json(patient_json: dict, i: int, list_j: list) -> list:
    """
    Parse a csv file of all vital signs measurements

    Parameters
    ----------
    patient_json
        The json file that contains information on a patient, loaded as a python dict
    i: int
        Increment to access a given encounter
    list_j:
        List of increments to access all vital_signs observations

    Returns
    -------
    list
        List containing all the parsed values, stored as a dictionary for each measurement.
        {variable_name: str, value: str, unit: str, time: str}
    """
    all_vital_signs_measures = []
    for j in list_j:
        observations = patient_json["record"]["encounters"][i]["observations"][j]
        if observations["observations"] != []:  # for specifically for blood_pressure
            observations = observations["observations"]
        else:
            observations = [observations]
        for observation in observations:
            try:
                variable = observation["codes"][0]["display"]
            except KeyError:
                variable = None

            try:
                value = observation["value"]
            except KeyError:
                value = None

            try:
                units = observation["unit"]
            except KeyError:
                units = None

            try:
                time = observation["start"]
                # convert sec to an actual date! last 3 digits represent the time zone
                time_sec = int(str(time)[:-3])
                # tzinfo = int(str(time)[-3:]) # how to convert country integer code to letter code??
                time = str(datetime.fromtimestamp(time_sec))
            except KeyError:
                time = None

            all_vital_signs_measures.append(
                {
                    "variable_name": variable,
                    "value": value,
                    "units": units,
                    "time": time,
                }
            )

    return all_vital_signs_measures


def parse_vital_signs_ccda(observations_on_specific_date: list) -> list:
    """
    Parse a ccda xml file of all vital signs measurements

    Parameters
    ----------
    observations_on_specific_date: list
        list of Elements

    Returns
    -------
    list
        List containing all the parsed values, stored as a dictionary for each measurement.
        {variable_name: str, value: str, unit: str, time: str}
    """
    all_vital_signs_measures = []

    for observation in observations_on_specific_date:
        variable = observation.find(".//{urn:hl7-org:v3}code").attrib["displayName"]
        value = observation.find(".//{urn:hl7-org:v3}value").attrib["value"]
        units = observation.find(".//{urn:hl7-org:v3}value").attrib["unit"]
        time = observation.find(".//{urn:hl7-org:v3}effectiveTime").attrib["value"]
        time = datetime.strptime(time, "%Y%m%d%H%M%S")
        time = datetime.isoformat(time)

        all_vital_signs_measures.append(
            {
                "variable_name": variable,
                "value": value,
                "units": units,
                "time": time,
            }
        )
    print(all_vital_signs_measures)
    return all_vital_signs_measures


def get_all_vital_signs_sql(connection: sqlite3.Connection, patient_id: str) -> pd.DataFrame:
    """
    Parse a sql file of all vital signs measurements

    Parameters
    ----------
    connection:
        Connection to sql data containing all vital signs
    patient_id: str
        External patient id

    Returns
    --------
    pd.DataFrame
        Pandas dataframe containing all vital signs (for all encounters)

    """
    cursor = connection.cursor()
    try:
        select_patient_vital_signs_query = "SELECT * FROM Observations WHERE patient = ? AND category = 'vital-signs'"
        cursor.execute(select_patient_vital_signs_query, (patient_id,))
        result = cursor.fetchall()
        if result:
            # Convert each tuple in the result to a dictionary
            column_names = [
                "date",
                "patient_id",
                "encounter_id",
                "category",
                "code",
                "variable_name",
                "value",
                "units",
                "type",
            ]
            vital_signs_unparsed = pd.DataFrame([dict(zip(column_names, row)) for row in result])
            return vital_signs_unparsed

        print(f"No vital signs found with ID {patient_id}")
        return None

    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None
    finally:
        cursor.close()


def parse_all_vital_signs_sql(vital_signs_enc_df: pd.DataFrame) -> list:
    """
    Parse a sql file of all vital signs measurements

    Parameters
    ----------
    vital_signs_enc_df: pd.DataFrame
        Pandas dataframe containing all vital signs for a specific encounter

    Returns
    -------
    list
        List containing all the parsed values, stored as a dictionary for each measurement.
        {variable_name: str, value: str, unit: str, time: str}
    """
    all_vital_signs_measures = []
    for _, vital_sign in vital_signs_enc_df.iterrows():
        try:
            variable = vital_sign["variable_name"]
        except KeyError:
            variable = None

        try:
            value = vital_sign["value"]
        except KeyError:
            value = None

        try:
            units = vital_sign["units"]
        except KeyError:
            units = None

        try:
            time = vital_sign["date"]
        except KeyError:
            time = None

        all_vital_signs_measures.append(
            {
                "variable_name": variable,
                "value": value,
                "units": units,
                "time": time,
            }
        )

    return all_vital_signs_measures


def parse_all_vital_signs_fhir() -> list:
    pass
