"""
Functions specific to the Vital Signs template
"""

from datetime import datetime
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional

from src.composition import datetime_now


class Measurement(BaseModel):
    """Data model for the Measurement class"""
    value: float = Field(..., serialization_alias='magnitude')
    units: str = Field(..., serialization_alias='units')
    time: datetime = Field(None, serialization_alias='timeValue')


class PointsInTime(BaseModel):
    """Data model for the PointsInTime class"""
    measurements: list[Measurement] = Field(..., serialization_alias='pointInTime')


class PointsInTime(BaseModel):
    """Data model for the PointsInTime class"""
    measurements: list[Measurement] = Field(..., serialization_alias='pointInTime')


class VitalSigns(BaseModel):
    """Data model for the VitalSigns class"""
    height: Optional[PointsInTime] = Field(None, serialization_alias='bodyHeightObservation')
    weight: Optional[PointsInTime] = Field(None, serialization_alias='bodyWeightObservation')
    heart_rate: Optional[PointsInTime] = Field(None, serialization_alias='heartRateObservation')
    blood_systolic: Optional[PointsInTime] = Field(None, serialization_alias='bloodPressureObservation')
    blood_diastolic: Optional[PointsInTime] = Field(None, serialization_alias='bloodPressureObservation')
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias='startTime')


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
        variable_name = measure['variable_name']

        if variable_name not in vital_signs_units.keys():
            # Keep only defined vital signs:
            continue
        try:
            value = float(measure['value'])
        except (ValueError, TypeError):
            value = None

        try:
            time = datetime.fromisoformat(measure['time']).isoformat()
        except TypeError:
            time = None

        if measure['units'] != vital_signs_units[variable_name]:
            print("Units of measurement is inconsistent.", end=' ')
            print(f"Units is in {measure['units']} but should be in {vital_signs_units[value]}.")
            units = None
            value = None
            time = None

        else:
            units = str(measure['units'])

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
        height=grouped_measures_pointintime['Body Height'],
        weight=grouped_measures_pointintime['Body Weight'],
        heart_rate=grouped_measures_pointintime['Heart rate'],
        blood_systolic=grouped_measures_pointintime['Systolic Blood Pressure'],
        blood_diastolic=grouped_measures_pointintime['Diastolic Blood Pressure']
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
            variable = vital_sign['DESCRIPTION']
        except KeyError:
            variable = None

        try:
            value = vital_sign['VALUE']
        except KeyError:
            value = None

        try:
            units = vital_sign['UNITS']
        except KeyError:
            units = None

        try:
            time = vital_sign['DATE']
        except KeyError:
            time = None

        all_vital_signs_measures.append({
            'variable_name': variable,
            'value': value,
            'units': units,
            'time': time
        })

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
        try:
            variable = patient_json['record']['encounters'][i]['observations'][j]['codes'][0]['display']
        except KeyError:
            variable = None

        try:
            value = patient_json['record']['encounters'][i]['observations'][j]['value']
        except KeyError:
            value = None

        try:
            units = patient_json['record']['encounters'][i]['observations'][j]['unit']
        except KeyError:
            units = None

        try:
            time = patient_json['record']['encounters'][i]['observations'][j]['start']
            # convert sec to an actual date! last 3 digits represent the time zone
            time_sec = int(str(time)[:-3])
            # tzinfo = int(str(time)[-3:]) # how to convert country integer code to letter code??
            time = str(datetime.fromtimestamp(time_sec))
        except KeyError:
            time = None

        all_vital_signs_measures.append({
            'variable_name': variable,
            'value': value,
            'units': units,
            'time': time
        })

    return all_vital_signs_measures
