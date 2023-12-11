"""
Post the vital_signs.opt template
Create a unique EHR for a patient
Create a composition per encounter using a JSON composition as an example
Post the compositions
"""

import re
from pathlib import Path

import click
import pandas as pd

from src.composition import post_composition, transform_composition
from src.diagnosis import parse_all_diagnosis
from src.ehr import create_ehr, fetch_all_ehr_id
from src.encounter import parse_all_encounters
from src.patient import parse_patient_csv, parse_patient_json, create_patient_attribute
from src.template import fetch_all_templates, post_template
from src.vitalsigns import  parse_vital_signs


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

    INPUT_FORMAT = 'json' # to set as an argument

    TEMPLATE_PATH = Path("data/templates")
    SYNTHEA_PATH = Path(f"data/{input_format}")


    print("\n\nSTEP 1 : POST templates")
    post_template(TEMPLATE_PATH / "vital_signs.opt")
    post_template(TEMPLATE_PATH / "patient.opt")
    post_template(TEMPLATE_PATH / "diagnosis_demo.opt")
    # fetch_all_templates()

    print("\n\nSTEP 2 : Create EHR for the first patient of the dataset")
    # patient_id = patients_df.iloc[0]["Id"]
    patient_id = "0a4a74f1-4444-6921-bf87-87fe209bec2e"
    ehr_id = create_ehr(patient_id)
    print(f"ehr_id: {ehr_id}")


    print("\n\nSTEP 3 : Extract Data")


    if input_format == 'csv':
        # Load datasets
        patients_df = pd.read_csv(SYNTHEA_PATH / "patients.csv")
        conditions_df = pd.read_csv(SYNTHEA_PATH / "conditions.csv")
        observations_df = pd.read_csv(SYNTHEA_PATH / "observations.csv")
        encounters_df = pd.read_csv(SYNTHEA_PATH / "encounters.csv")

        all_encounters = parse_all_encounters(encounters_df)

        print("\nPatient composition..")
        patient_raw_data = patients_df[patients_df["Id"] == patient_id]
        patient = create_patient_attribute(*parse_patient_csv(patient_raw_data))


    elif input_format == 'json':
        # Load json patient file as a python dictionary
        with open(SYNTHEA_PATH / f"{patient_id}.json") as infile:
            patient_json = json.load(infile)

        print("\nPatient composition..")
        create_patient_attribute(*parse_patient_json(patient_json))





    print("\n\nSTEP 4 : Transform and Load compositions")

    patient_json_str = patient.model_dump_json(by_alias=True, indent=4)
    print(f"\npatient: {patient_json_str}")
    patient_composition = transform_composition(patient.model_dump_json(by_alias=True), "patient")
    print(f"\ncomposition: {patient_composition}")

    patient_composition_uuid = post_composition(ehr_id, patient_composition)
    print(f"\npatient_composition_uuid: {patient_composition_uuid}")

        # print("\nVital Signs compositions..")
        # vitalsigns_variables = [
        #     {'name': 'Body Height', 'units': 'cm'},
        #     # {'name': 'Body Weight', 'units': 'kg'},
        #     # {'name': 'Heart rate', 'units': '/min'},
        #     # {'name': 'Systolic Blood Pressure', 'units': 'mm[Hg]'},
        #     # {'name': 'Diastolic Blood Pressure', 'units': 'mm[Hg]'}
        # ]

        # patient_encounter_ids = [encounter_id for encounter_id, encounter in all_encounters.items() if
        #                          encounter.patient_id == patient_id]
        # # patient_encounter_ids = encounters_df[encounters_df["PATIENT"] == patient_id]["Id"].tolist()
        # for encounter_id in patient_encounter_ids:
        #     vitalsigns_df = observations_df[
        #         (observations_df["ENCOUNTER"] == encounter_id) & \
        #         (observations_df["CATEGORY"] == "vital-signs") & \
        #         (observations_df["DESCRIPTION"].isin([v["name"] for v in vitalsigns_variables]))
        #         ]

        #     if vitalsigns_df.shape[0] == 0:
        #         # print(f"Encounter id {encounter_id} has no vital signs observations")
        #         continue

        #     vitalsigns = parse_vital_signs(vitalsigns_df, vitalsigns_variables)
        #     vitalsigns_json_str = vitalsigns.model_dump_json(by_alias=True, indent=4)
        #     print(f"\ndiagnosis: {vitalsigns_json_str}")
        #     vitalsigns_composition = transform_composition(vitalsigns.model_dump_json(by_alias=True), "vital_signs")
        #     # print(f"\ncomposition: {vitalsigns_composition}")

        #     vitalsigns_composition_uuid = post_composition(ehr_id, vitalsigns_composition)
        #     print(f"\ndiagnosis_composition_uuid: {vitalsigns_composition_uuid}")

        # # plot_bloodpressure_over_time(ehr_id)

        # print("\nDiagnosis compositions..")
        # where_disorder = conditions_df.DESCRIPTION.apply(lambda x: bool(re.search('.*(disorder)', x)))
        # conditions_df = conditions_df[where_disorder]
        # patient_diagnosis_df = conditions_df[conditions_df["PATIENT"] == patient_id]
        # for _, diagnosis_df in patient_diagnosis_df.iterrows():
        #     diagnosis = parse_all_diagnosis(diagnosis_df)
        #     diagnosis_json_str = diagnosis.model_dump_json(by_alias=True, indent=4)
        #     print(f"\ndiagnosis: {diagnosis_json_str}")
        #     diagnosis_composition = transform_composition(diagnosis.model_dump_json(by_alias=True), "diagnosis-demo")
        #     # print(f"\ncomposition: {diagnosis_composition}")

        #     diagnosis_composition_uuid = post_composition(ehr_id, diagnosis_composition)
        #     print(f"\ndiagnosis_composition_uuid: {diagnosis_composition_uuid}")


@click.group()
def cli():
    pass


cli.add_command(run)
cli.add_command(list_all_templates)
cli.add_command(get_all_ehr_id)

if __name__ == "__main__":
    cli()
