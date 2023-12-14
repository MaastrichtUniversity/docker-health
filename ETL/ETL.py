"""
Post the vital_signs.opt template
Create a unique EHR for a patient
Create a composition per encounter using a JSON composition as an example
Post the compositions
"""

import os
from pathlib import Path
import click

from src.template import fetch_all_templates, post_template
from src.ehr import create_ehr, fetch_all_ehr_id
from src.etl import (
    extract_all_csv,
    extract_all_json,
    transform_load
)

# config:
PATIENT_ID = '0a4a74f1-4444-6921-bf87-87fe209bec2e'
INPUT_FORMAT = 'json'
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
        patient, all_disorders, all_vital_signs = extract_all_csv(
            patient_id=PATIENT_ID,
            data_path=SYNTHEA_PATH,
            vital_signs_units=VITAL_SIGNS_UNITS
        )

    elif INPUT_FORMAT == 'json':
        patient, all_disorders, all_vital_signs = extract_all_json(
            patient_id=PATIENT_ID,
            data_path=SYNTHEA_PATH,
            vital_signs_units=VITAL_SIGNS_UNITS
        )


    print("\n\nSTEP 4 : Transform and Load compositions")
    transform_load(
        patient=patient,
        all_disorders=all_disorders,
        all_vital_signs=all_vital_signs,
        ehr_id=EHR_ID,
        output_path=COMPOSITION_OUTPUT_PATH
    )


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
