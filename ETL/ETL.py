"""
Post the vital_signs.opt template
Create a unique EHR for a patient
Create a composition per encounter using a JSON composition as an example
Post the compositions
"""

import re
from pathlib import Path
import pandas as pd
import click
import pytz
from datetime import datetime


from src.template import fetch_all_templates, post_template
from src.ehr import create_ehr, fetch_all_ehr_id
from src.composition import load_composition_example, update_composition_high_level, post_composition
from src.encounter import parse_all_encounters
from src.patient import parse_patient, update_composition_patient
from src.diagnosis import parse_all_diagnosis, update_composition_diagnosis
from src.vitalsigns import (
    parse_vitalsigns,
    update_composition_vitalsigns,
    plot_bloodpressure_over_time,
)

NLTZ = pytz.timezone('Europe/Amsterdam')


@click.command(help="Get all EHR ID on a specific openEHR instance")
def get_all_ehr_id():
    """This function is a proxy for the click command to interact with the above fetch_all_ehr_id function."""
    ehr_ids = fetch_all_ehr_id()
    for i in ehr_ids:
        click.echo(i)


@click.command(help="Print all template available on the server")
def list_all_templates():
    """This function is a proxy for the click command to interact with the above fetch_all_templates function."""
    fetch_all_templates()


@click.command(help="Runs all ETL from default hard coded values")
def run():
    """Runs the ETL"""

    TEMPLATE_PATH = Path("data/templates")
    SYNTHEA_PATH = Path("data/synthea_csv")
    COMPOSITION_PATH = Path("data/compositions/locatable")

    # Load datasets
    patients_df = pd.read_csv(SYNTHEA_PATH / "patients.csv")
    conditions_df = pd.read_csv(SYNTHEA_PATH / "conditions.csv")
    observations_df = pd.read_csv(SYNTHEA_PATH / "observations.csv")
    encounters_df = pd.read_csv(SYNTHEA_PATH / "encounters.csv")

    all_encounters = parse_all_encounters(encounters_df)

    print("\n\nSTEP 1 : POST templates")
    post_template(TEMPLATE_PATH / "vital_signs.opt")
    post_template(TEMPLATE_PATH / "patient.opt")
    post_template(TEMPLATE_PATH / "diagnosis_demo.opt")
    # fetch_all_templates()


    print("\n\nSTEP 2 : Create EHR for the first patient of the dataset")
    patient_id = patients_df.iloc[0]["Id"]
    ehr_id = create_ehr(patient_id)
    # all_ehr_ids = fetch_all_ehr_id()


    print("\n\nSTEP 3 : Create compositions:")

    print("\nPatient composition..")
    patient = parse_patient(patients_df[patients_df["Id"] == patient_id])
    patient_composition = load_composition_example(COMPOSITION_PATH / "patient_20231122085524_000001_1.json")
    patient_composition = update_composition_patient(patient_composition, patient)
    patient_composition = update_composition_high_level(patient_composition, datetime.now(NLTZ).isoformat())
    response = post_composition(ehr_id, patient_composition)


    print("\nVital Signs compositions..")
    vitalsigns_variables = [
        {'name': 'Body Height', 'units': 'cm'},
        {'name': 'Body Weight', 'units': 'kg'},
        {'name': 'Heart rate', 'units': '/min'},
        {'name': 'Systolic Blood Pressure', 'units': 'mm[Hg]'},
        {'name': 'Diastolic Blood Pressure', 'units': 'mm[Hg]'}
    ]

    patient_encounter_ids = [encounter_id for encounter_id, encounter in all_encounters.items() if encounter.patient_id == patient_id]
    # patient_encounter_ids = encounters_df[encounters_df["PATIENT"] == patient_id]["Id"].tolist()
    all_vitalsigns = {}
    for encounter_id in patient_encounter_ids:
        vitalsigns_df = observations_df[
            (observations_df["ENCOUNTER"] == encounter_id) & \
            (observations_df["CATEGORY"] == "vital-signs") & \
            (observations_df["DESCRIPTION"].isin([v["name"] for v in vitalsigns_variables]))
        ]

        if vitalsigns_df.shape[0] == 0:
            # print(f"Encounter id {encounter_id} has no vital signs observations")
            continue
        
        all_vitalsigns[encounter_id] = parse_vitalsigns(vitalsigns_df, vitalsigns_variables)
        vitalsigns_composition = load_composition_example(COMPOSITION_PATH / "vital_signs_20231122085528_000001_1.json")
        vitalsigns_composition = update_composition_vitalsigns(vitalsigns_composition, all_vitalsigns[encounter_id])
        vitalsigns_composition = update_composition_high_level(vitalsigns_composition, all_encounters[encounter_id].startdate)
        reponse = post_composition(ehr_id, vitalsigns_composition)

    # plot_bloodpressure_over_time(ehr_id)


    print("\nDiagnosis compositions..")
    where_disorder = conditions_df.DESCRIPTION.apply(lambda x: bool(re.search('.*(disorder)', x)))
    conditions_df = conditions_df[where_disorder]
    patient_diagnosis_df = conditions_df[conditions_df["PATIENT"] == patient_id]
    all_diagnosis = {}
    for _, diagnosis_df in patient_diagnosis_df.iterrows():
        encounter_id = diagnosis_df["ENCOUNTER"]
        all_diagnosis[encounter_id] = parse_all_diagnosis(diagnosis_df)

    for encounter_id, diagnosis in all_diagnosis.items():
        diagnosis_composition = load_composition_example(COMPOSITION_PATH / "diagnosis_demo_20231122085526_000001_1.json")
        diagnosis_composition = update_composition_diagnosis(diagnosis_composition,  all_diagnosis[encounter_id])
        diagnosis_composition = update_composition_high_level(diagnosis_composition, all_encounters[encounter_id].startdate)
        response = post_composition(ehr_id, diagnosis_composition)

    # RESPONSE: 422
    # ERROR Unprocessable Entity
    # /content[openEHR-EHR-EVALUATION.problem_diagnosis.v1 and
    # name/value='Diagnosis']/data[at0001]/items[at0002 and name/value='Diagnosis']/value:
    # CodePhrase codeString does not match any option, found: 312608009


@click.group()
def cli():
    pass

cli.add_command(run)
cli.add_command(list_all_templates)
cli.add_command(get_all_ehr_id)

if __name__ == "__main__":
    cli()
