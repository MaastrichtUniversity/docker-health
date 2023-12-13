"""
Functions specific to AQL queries and plotting
"""

import os
import json
from pathlib import Path
from uuid import UUID
import requests
import pandas as pd
import matplotlib.pyplot as plt

EHRBASE_USERRNAME = os.environ['EHRBASE_USERRNAME']
EHRBASE_PASSWORD = os.environ['EHRBASE_PASSWORD']
EHRBASE_BASE_URL = os.environ['EHRBASE_BASE_URL']

PLOT_PATH = Path('data/plot')

def plot_bloodpressure_over_time(ehr_id: UUID) -> None:
    """
    Plot and save a graph of systolic and diastolic bloodpressure
    for a given patient using the vital signs template.

    Parameters
    ----------
    ehr_id: UUID
        ehr_id of the patient for which the data will be plotted

    """
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = f"SELECT c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/time as time,  c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0004]/value/magnitude as systolic ,  c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0005]/value/magnitude as diastolic FROM EHR e CONTAINS COMPOSITION c WHERE c/archetype_details/template_id/value='Vital signs' AND e/ehr_id/value='{ehr_id}'"
    headers = {
        'Accept': 'application/json',
        'Prefer': 'return=representation',
    }
    response = requests.request(
        'GET',
        url,
        headers=headers,
        params={'q': query},
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10
    )
    response_json = json.loads(response.text)
    dataframe = pd.DataFrame(columns=['Time', 'Systolic', 'Diastolic'])

    for row in response_json['rows']:
        dataframe.loc[len(dataframe)] = [row[0]['value'], row[1], row[2]]

    dataframe['Time'] = pd.to_datetime(dataframe['Time'])
    dataframe = dataframe.sort_values(by='Time')
    dataframe.set_index('Time', inplace=True)
    dataframe.plot()

    plt.savefig(PLOT_PATH / f"{ehr_id}_bloodpressure_over_time.png")
    plt.close()
