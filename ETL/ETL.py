"""
Post the vital_signs.opt template
Create a unique EHR for a patient
Create a composition per encounter using a JSON composition as an example
Post the compositions
"""

import os
import re
from pathlib import Path
import json
import click
import pandas as pd
import sqlite3

from src.template import fetch_all_templates, post_template
from src.ehr import create_ehr, fetch_all_ehr_id
from src.composition import (
    transform_composition,
    post_composition,
    write_json_composition
)

from src.patient import (
    parse_patient_csv,
    parse_patient_json,
    create_patient_instance, parse_patient_sql
)
from src.diagnosis import (
    parse_all_diagnosis_csv,
    parse_all_diagnosis_json,
    create_diagnosis_instance, get_all_diagnosis_sql, parse_diagnosis_sql
)
from src.vitalsigns import (
    parse_vital_signs_csv,
    parse_vital_signs_json,
    create_vital_signs_instance, get_all_vital_signs_sql
)

# arguments:
PATIENT_ID = 'f78a8b0a-7deb-9ee5-8138-6eec00a8a6bd'
INPUT_FORMAT = 'sql'


TEMPLATE_PATH = Path("data/templates")
SYNTHEA_PATH = Path(f"data/synthea/{INPUT_FORMAT}")
COMPOSITION_OUTPUT_PATH = Path("outputs/compositions") / PATIENT_ID
os.makedirs(COMPOSITION_OUTPUT_PATH, exist_ok=True)

VITAL_SIGNS_UNITS = {
    'Body Height': 'cm',
    'Body Weight': 'kg',
    'Heart rate': '/min',
    # {'name': 'Systolic Blood Pressure', 'units': 'mm[Hg]'},
    # {'name': 'Diastolic Blood Pressure', 'units': 'mm[Hg]'}
}


def extract_all_csv():
    """
    TODO
    """
    # Load datasets
    patients_df = pd.read_csv(SYNTHEA_PATH / 'patients.csv')
    conditions_df = pd.read_csv(SYNTHEA_PATH / 'conditions.csv')
    observations_df = pd.read_csv(SYNTHEA_PATH / 'observations.csv')
    encounters_df = pd.read_csv(SYNTHEA_PATH / 'encounters.csv')
    # all_encounters = parse_all_encounters(encounters_df)

    print("\nPatient..", end='\t')
    patient_df = patients_df[patients_df['Id'] == PATIENT_ID]
    patient = create_patient_instance(*parse_patient_csv(patient_df))
    print(f"information extracted for patient_id: {PATIENT_ID}")

    print("\nDiagnosis..", end='\t')
    where_disorder = conditions_df['DESCRIPTION'].apply(
        lambda x: bool(re.search('.*(disorder)', x))
    )
    patient_disorders_df = conditions_df[where_disorder][conditions_df['PATIENT'] == PATIENT_ID]
    all_disorders = []
    for _, disorder_df in patient_disorders_df.iterrows():
        all_disorders.append(create_diagnosis_instance(*parse_all_diagnosis_csv(disorder_df)))
    print(f"{len(all_disorders)} disorders reported for this patient.")

    print("\nVital Signs..", end='\t')
    patient_encounter_ids = encounters_df[encounters_df['PATIENT'] == PATIENT_ID]['Id'].tolist()
    vital_signs_df = observations_df[
        (observations_df['ENCOUNTER'].isin(patient_encounter_ids)) & \
        (observations_df['CATEGORY'] == 'vital-signs')
        # (observations_df['DESCRIPTION'].isin(VITAL_SIGNS_UNITS.keys()))
    ]

    all_vital_signs = []
    for encounter_id in patient_encounter_ids:
        vital_signs_enc_df = vital_signs_df[vital_signs_df['ENCOUNTER'] == encounter_id]
        if vital_signs_enc_df.shape[0] == 0:
            # print(f"Encounter id {encounter_id} has no vital signs observations")
            continue

        all_vital_signs.append(create_vital_signs_instance(
            parse_vital_signs_csv(vital_signs_enc_df),
            VITAL_SIGNS_UNITS
        ))

    print(f"{len(all_vital_signs)} vital signs reported for this patient.")

    return patient, all_disorders, all_vital_signs

def extract_all_json():
    """
    TODO
    """
    # Load json patient file as a python dictionary
    with open(SYNTHEA_PATH / f"{PATIENT_ID}.json", encoding='utf-8') as infile:
        patient_json = json.load(infile)

    print("\nPatient..", end='\t')
    patient = create_patient_instance(*parse_patient_json(patient_json))
    print(f"information extracted for patient_id: {PATIENT_ID}")

    print("\nDiagnosis..", end='\t')
    all_disorders = []
    for encounter_i, encounter in enumerate(patient_json['record']['encounters']):
        if 'conditions' in encounter:
            for condition_j, condition in enumerate(encounter['conditions']):
                description = condition['codes'][0]['display']
                if not bool(re.search('.*(disorder)', description)):
                    # print("Current condition is not classified as a disorder.")
                    continue
                all_disorders.append(create_diagnosis_instance(
                    *parse_all_diagnosis_json(patient_json, encounter_i, condition_j))
                )
    print(f"{len(all_disorders)} disorders reported for this patient.")

    print("\nVital Signs..")
    all_vital_signs = []
    for encounter_i, encounter in enumerate(patient_json['record']['encounters']):
        if encounter['observations'] == []:
            # print(f"Encounter id {encounter_i} has no vital signs observations")
            continue
        list_observations_j = []
        for observation_j, observation in enumerate(encounter['observations']):
            if observation['category'] == 'vital-signs':
                list_observations_j.append(observation_j)

        all_vital_signs.append(create_vital_signs_instance(
            parse_vital_signs_json(patient_json, encounter_i, list_observations_j),
            VITAL_SIGNS_UNITS
        ))
    print(f"{len(all_vital_signs)} vital signs reported for this patient.")

    return patient, all_disorders, all_vital_signs

def extract_all_sql():
    print("\nPatient..", end='\t')
    connection = sqlite3.connect(SYNTHEA_PATH / "patients.sqlite")
    patient = create_patient_instance(*parse_patient_sql(connection, PATIENT_ID))
    connection.close()

    print(f"\n\nDiagnosis...")
    connection = sqlite3.connect(SYNTHEA_PATH / "conditions.sqlite")
    patient_diagnosis_sql = get_all_diagnosis_sql(connection, PATIENT_ID)
    all_diagnosis = []
    for diagnosis in patient_diagnosis_sql:
        all_diagnosis.append(create_diagnosis_instance(*parse_diagnosis_sql(diagnosis)))


    print("\nVital Signs..", end='\t')
    connection = sqlite3.connect(SYNTHEA_PATH / "observations.sqlite")
    vital_signs = create_vital_signs_instance(get_all_vital_signs_sql(connection, PATIENT_ID), VITAL_SIGNS_UNITS)
    # transform load function currently expect a list
    all_vital_signs = []
    all_vital_signs.append(vital_signs)
    connection.close()

    return patient, all_diagnosis, all_vital_signs


def transform_load(patient, all_disorders, all_vital_signs):
    """
    TODO
    """
    print("\nPatient..")
    patient_json_str = patient.model_dump_json(by_alias=True, indent=4)
    print(f"\npatient: {patient_json_str}")
    patient_composition = transform_composition(patient.model_dump_json(by_alias=True), 'patient')
    # print(f"\ncomposition: {patient_composition}")
    write_json_composition(
        composition=patient_composition,
        json_filename=COMPOSITION_OUTPUT_PATH / 'patient.json'
    )
    patient_composition_uuid = post_composition(EHR_ID, patient_composition)
    print(f"\npatient_composition_uuid: {patient_composition_uuid}")

    print("\nDiagnosis..")
    for diagnosis_i, diagnosis in enumerate(all_disorders):
        diagnosis_json_str = diagnosis.model_dump_json(by_alias=True, indent=4)
        print(f"\ndiagnosis {diagnosis_i+1}: {diagnosis_json_str}")
        diagnosis_composition = transform_composition(
            diagnosis.model_dump_json(by_alias=True), "diagnosis-demo"
        )
        write_json_composition(
            composition=diagnosis_composition,
            json_filename=COMPOSITION_OUTPUT_PATH / f'diagnosis_{diagnosis_i+1}.json'
        )
        # print(f"\ncomposition: {diagnosis_composition}")
        diagnosis_composition_uuid = post_composition(EHR_ID, diagnosis_composition)
        print(f"diagnosis_composition_uuid: {diagnosis_composition_uuid}")

    print("\nVital Signs..")

    for vitalsigns_i, vitalsigns in enumerate(all_vital_signs):
        vitalsigns_json_str = vitalsigns.model_dump_json(by_alias=True, indent=4)
        print(f"\nvital_signs {vitalsigns_i+1}: {vitalsigns_json_str}")
        vitalsigns_composition = transform_composition(
            vitalsigns.model_dump_json(by_alias=True), 'vital_signs'
        )
        write_json_composition(
            composition=vitalsigns_composition,
            json_filename=COMPOSITION_OUTPUT_PATH / f'vital_signs_{vitalsigns_i+1}.json'
        )
        # print(f"\ncomposition: {vitalsigns_composition}")
        vitalsigns_composition_uuid = post_composition(EHR_ID, vitalsigns_composition)
        print(f"diagnosis_composition_uuid: {vitalsigns_composition_uuid}")



@click.command(help="Get all EHR ID on a specific openEHR instance")
def get_all_ehr_id():
    """proxy for the click command to interact with the above fetch_all_ehr_id function."""
    ehr_ids = fetch_all_ehr_id()
    for i in ehr_ids:
        click.echo(i)


@click.command(help="Print all template available on the server")
def list_all_templates():
    """proxy for the click command to interact with the above fetch_all_templates function."""
    fetch_all_templates()


@click.command(help="Runs all ETL from default hard coded values")
def run():
    """Runs the ETL"""

    print("\n\nSTEP 1 : POST templates")
    post_template(TEMPLATE_PATH / 'vital_signs.opt')
    post_template(TEMPLATE_PATH / 'patient.opt')
    post_template(TEMPLATE_PATH / 'diagnosis_demo.opt')
    # fetch_all_templates()


    print(f"\n\nSTEP 2 : Create EHR for the patient_id {PATIENT_ID}")
    global EHR_ID
    EHR_ID = create_ehr(PATIENT_ID)
    print(f"ehr_id: {EHR_ID}")


    print(f"\n\nSTEP 3 : Data extraction from {INPUT_FORMAT} input data format")
    if INPUT_FORMAT == 'csv':
        patient, all_disorders, all_vital_signs = extract_all_csv()
    elif INPUT_FORMAT == 'json':
        patient, all_disorders, all_vital_signs = extract_all_json()
    elif INPUT_FORMAT == 'sql':
        patient, all_disorders, all_vital_signs = extract_all_sql()


    print("\n\nSTEP 4 : Transform and Load compositions")
    transform_load(patient, all_disorders, all_vital_signs)


    # print("\n\nSTEP 5 : Analysis insights")
    # plot_bloodpressure_over_time(ehr_id)


@click.group()
def cli():
    pass


cli.add_command(run)
cli.add_command(list_all_templates)
cli.add_command(get_all_ehr_id)

if __name__ == "__main__":
    cli()
