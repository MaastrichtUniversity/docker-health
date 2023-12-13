"""
Functions specific to the Vital Signs template
"""

from datetime import datetime
import pandas as pd
from pydantic import BaseModel, Field

from src.composition import datetime_now


class Measurement(BaseModel):
    """Data model for measurement"""
    value: float = Field(..., serialization_alias='magnitude')
    units: str = Field(..., serialization_alias='units')
    time: datetime = Field(None, serialization_alias='timeValue')


class PointsInTime(BaseModel):
    """TODO"""
    measurements: list[Measurement] = Field(..., serialization_alias='pointInTime')


class VitalSigns(BaseModel):
    """Data model for the vital signs"""

    height: PointsInTime = Field(..., serialization_alias='bodyHeightObservation')
    weight: PointsInTime = Field(..., serialization_alias='BodyWeightObservation')
    heart_rate: PointsInTime = Field(..., serialization_alias='HeartRateObservation')
    # blood_systolic: PointsInTime = Field(..., serialization_alias='BloodPressureObservation')
    # blood_diastolic: PointsInTime = Field(..., serialization_alias='BloodPressureObservation')
    start_time: datetime = Field(default_factory=datetime_now, serialization_alias='startTime')


def create_vital_signs_instance(all_vital_signs_measures: list, vital_signs_units: list) -> VitalSigns:
    """
    check format (ISO and local terms) and create a Diagnosis attribute
    TO DO
    """
    grouped_measures = {}

    for measure in all_vital_signs_measures:
        variable_name = measure['variable_name']

        if variable_name not in vital_signs_units.keys():
            continue
        try:
            value = float(measure['value'])
        except (ValueError, TypeError):
            value = None

        try:
            time = datetime.fromisoformat(measure['time']).isoformat()
        except TypeError:
            time = None

        if vital_signs_units[variable_name] != measure['units']:
            print("measurement units is inconsistent.", end=' ')
            print(f"Units is in {measure['units']} but should be in {vital_signs_units[value]}.")
            units = None
            value = None
            time = None

        else:
            units = str(measure['units'])

        if variable_name not in grouped_measures:
            grouped_measures[variable_name] = []
        grouped_measures[variable_name].append(Measurement(value=value, units=units, time=time))

    height = PointsInTime(measurements=grouped_measures['Body Height'])
    weight = PointsInTime(measurements=grouped_measures['Body Weight'])
    heart_rate = PointsInTime(measurements=grouped_measures['Heart rate'])
    # 'Systolic Blood Pressure'
    # 'Diastolic Blood Pressure'

    return VitalSigns(height=height, weight=weight, heart_rate=heart_rate)


def parse_vital_signs_csv(vital_signs_enc_df: pd.DataFrame):
    """
    Parse vital signs dataframe to a vital signs class
    Parameters
    ----------
    vital_signs_df
        Pandas dataframe that contains the values for the vital signs for a single encounter

    Returns
    -------
    VitalSigns
        Instance of VitalSigns filled with the values

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


def parse_vital_signs_json(patient_json: dict, i: int, list_j: list):
    """
    TODO
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
