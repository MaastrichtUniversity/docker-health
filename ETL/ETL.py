"""
Post the vital_signs.opt template
Create a unique EHR for a patient
Create a composition per emcounter using a JSON composition as an example
Post the compositions
"""

import re
from pathlib import Path
import pandas as pd
import click

from src.template import fetch_all_templates, post_template
from src.ehr import create_ehr, fetch_all_ehr_id
from src.composition import load_composition_example, update_composition_high_level, post_composition
from src.patient import parse_patient
from src.diagnosis import parse_all_diagnosis
from src.vitalsigns import (
    parse_vital_signs,
    update_composition_vital_signs,
    remove_pulse_oximetry_from_composition,
    plot_bloodpressure_over_time,
)


@click.command(help="Get all EHR ID on a specific openEHR instance")
def get_all_ehr_id():
    """This function is a proxy for the click command to interact with the above fetch_all_ehr_id function."""
    ehr_ids = fetch_all_ehr_id()
    for id in ehr_ids:
        click.echo(id)


@click.command(help="Print all template available on the server")
def list_all_templates():
    """This function is a proxy for the click command to interact with the above fetch_all_templates function."""
    fetch_all_templates()


@click.command(help="Runs all ETL from default hard coded values")
def run():
    """Runs the ETL"""
    TEMPLATE_PATH = Path("data/templates")
    SYNTHEA_PATH = Path("data/synthea_csv")
    # COMPOSITION_PATH = Path("data/composition")
    # EXAMPLE_COMPOSITION = "vital_signs_20231025075308_000001_1.json"

    # Load datasets
    patients_df = pd.read_csv(SYNTHEA_PATH / "patients.csv")
    conditions_df = pd.read_csv(SYNTHEA_PATH / "conditions.csv")
    observations_df = pd.read_csv(SYNTHEA_PATH / "observations.csv")
    encounters_df = pd.read_csv(SYNTHEA_PATH / "encounters.csv")

    # POST templates
    post_template(TEMPLATE_PATH / "vital_signs.opt")
    post_template(TEMPLATE_PATH / "patient.opt")
    post_template(TEMPLATE_PATH / "diagnosis_demo.opt")
    # fetch_all_templates()

    # Create EHR for the first patient of the dataset
    patient_id = patients_df.iloc[0]["Id"]
    ehr_id = create_ehr(patient_id)
    # all_ehr_ids = fetch_all_ehr_id()

    # Create compositions:
    ## PATIENT COMPOSITION
    patient = parse_patient(patients_df[patients_df["Id"] == patient_id])
    # composition = load_composition_example(COMPOSITION_PATH / EXAMPLE_COMPOSITION)
    # composition = update_composition_high_level(composition, encounter_start, encounter_stop)
    # composition = update_composition_patient(composition, vital_signs_class)


    ## DIAGNOSIS COMPOSITION
    where_disorder = conditions_df.DESCRIPTION.apply(lambda x: bool(re.search('.*(disorder)', x)))
    conditions_df = conditions_df[where_disorder]
    patient_diagnosis_df = conditions_df[conditions_df["PATIENT"] == patient_id]
    all_diagnosis = {}
    for _, diagnosis_df in patient_diagnosis_df.iterrows():
        encounter_id = diagnosis_df["ENCOUNTER"]
        all_diagnosis[encounter_id] = parse_all_diagnosis(diagnosis_df)
    # composition = load_composition_example(COMPOSITION_PATH / EXAMPLE_COMPOSITION)
    # composition = update_composition_high_level(composition, encounter_start, encounter_stop)
    # composition = update_composition_patient(composition, vital_signs_class)


    ## VITAL SIGNS COMPOSITION
    patient_encounters_ids = encounters_df[encounters_df["PATIENT"] == patient_id]["Id"].tolist()

    all_vital_signs = {}
    for encounter_id in patient_encounter_ids:
        vital_signs_df = observations_df[
            (observations_df["ENCOUNTER"] == encounter_id) & (observations_df["CATEGORY"] == "vital-signs")
        ]

        if vital_signs_df.shape[0] == 0:
            print(f"{encounter_id} has no vital signs observations")
            continue
        else:
            all_vital_signs[encounter_id] = parse_vital_signs(vital_signs_df)

        # encounter_start = encounters_df.loc[encounters_df["Id"] == encounter_id]["START"].values[0]
        # encounter_stop = encounters_df.loc[encounters_df["Id"] == encounter_id]["STOP"].values[0]
        # composition = load_composition_example(COMPOSITION_PATH / EXAMPLE_COMPOSITION)
        # composition = update_composition_high_level(composition, encounter_start, encounter_stop)
        composition = update_composition_vital_signs(composition, vital_signs_class)
        composition = remove_pulse_oximetry_from_composition(composition)
        post_composition(ehr_id, composition)

    plot_bloodpressure_over_time(ehr_id)


@click.group()
def cli():
    pass

cli.add_command(run)
cli.add_command(list_all_templates)
cli.add_command(get_all_ehr_id)

if __name__ == "__main__":
    cli()
