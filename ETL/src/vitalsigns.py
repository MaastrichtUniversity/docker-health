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


def parse_vital_signs_csv(vital_signs_df: pd.DataFrame) -> VitalSigns:
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

    measurements = {}

    for _, vital_sign in vital_signs_df.iterrows():
        value = vital_sign['VALUE']
        units = vital_sign['UNITS']
        time = vital_sign['DATE']
        if variable in measurements:
            measurements[vital_sign['DESCRIPTION']].append((value, units, time))
        else:
            measurements[vital_sign['DESCRIPTION']] = [(value, units, time)]

    return variable, value, unit, start_date


    #     if variable['name'] == 'Body Height':
    #         measurements['height'].append(Measurement(value=value, units=units, time=time))
    #     if variable['name'] == 'Body Weight':
    #         measurements['weight'].append(Measurement(value=value, units=units, time=time))
    #     if variable['name'] == 'Heart rate':
    #         measurements['heart_rate'].append(Measurement(value=value, units=units, time=time))
    #     # if variable['name'] == 'Systolic Blood Pressure':
    #     #     vital_signs.blood_systolic = measure_instance
    #     # if variable['name'] == 'Diastolic Blood Pressure':
    #     #     vital_signs.blood_diastolic = measure_instance
    # height = PointsInTime(measurements=measurements['height'])
    # weight = PointsInTime(measurements=measurements['weight'])
    # heart_rate = PointsInTime(measurements=measurements['heart_rate'])

    return VitalSigns(height=height, weight=weight, heart_rate=heart_rate)


def parse_vital_signs_json(patient_json: dict, i: int, j: int):
    """
    TODO
    """
    try:
        variable = patient_json['record']['encounters'][i]['observations'][j]['codes'][0]['display']
    except KeyError:
        variable = None

    try:
        value = patient_json['record']['encounters'][i]['observations'][j]['value']
    except KeyError:
        value = None

    try:
        unit = patient_json['record']['encounters'][i]['observations'][j]['unit']
    except KeyError:
        unit = None

    try:
        start_date = patient_json['record']['encounters'][i]['observations'][j]['start']
        # convert sec to an actual date! last 3 digits represent the time zone
        start_date_sec = int(str(start_date)[:-3])
        # tzinfo = int(str(start_date)[-3:]) # how to convert country integer code to letter code??
        start_date = datetime.fromtimestamp(start_date_sec)
    except KeyError:
        start_date = None

    return variable, value, unit, start_date
