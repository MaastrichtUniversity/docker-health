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
    extract_all_ccda,
    extract_all_sql,
    extract_all_fhir,
    transform_load,
)


# config:
PATIENT_ID = "3b1dadde-eefe-e82a-efbc-daa3c959a0c2"
TEMPLATE_PATH = Path("data/templates")
VITAL_SIGNS_UNITS = {
    "Body Height": "cm",
    "Body Weight": "kg",
    "Heart rate": "/min",
    "Systolic Blood Pressure": "mm[Hg]",
    "Diastolic Blood Pressure": "mm[Hg]",
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


@click.command(help="Runs all ETL for a single patient. [Accepted input_format: csv, sql, json, ccda, fhir]")
@click.argument("input_format")
def run(input_format):
    """Runs the ETL"""
    synthea_path = Path(f"data/synthea/{input_format}")
    composition_output_path = Path("outputs/compositions") / PATIENT_ID / input_format
    os.makedirs(composition_output_path, exist_ok=True)

    print("\n\nSTEP 1 : POST templates")
    post_template(TEMPLATE_PATH / "vital_signs.opt")
    post_template(TEMPLATE_PATH / "patient.opt")
    post_template(TEMPLATE_PATH / "diagnosis_demo.opt")
    # fetch_all_templates()

    print(f"\n\nSTEP 2 : Create EHR for the patient_id {PATIENT_ID}")
    global EHR_ID
    EHR_ID = create_ehr(PATIENT_ID)
    print(f"ehr_id: {EHR_ID}")

    print(f"\n\nSTEP 3 : Data extraction from {input_format} input data format")
    if input_format == "csv":
        patient, all_disorders, all_vital_signs = extract_all_csv(
            patient_id=PATIENT_ID,
            data_path=synthea_path,
            vital_signs_units=VITAL_SIGNS_UNITS,
        )
    elif input_format == "json":
        patient, all_disorders, all_vital_signs = extract_all_json(
            patient_id=PATIENT_ID,
            data_path=synthea_path,
            vital_signs_units=VITAL_SIGNS_UNITS,
        )
    elif input_format == "ccda":
        patient, all_disorders, all_vital_signs = extract_all_ccda(
            patient_id=PATIENT_ID,
            data_path=synthea_path,
            vital_signs_units=VITAL_SIGNS_UNITS,
        )
    elif input_format == "sql":
        patient, all_disorders, all_vital_signs = extract_all_sql(
            patient_id=PATIENT_ID,
            data_path=synthea_path,
            vital_signs_units=VITAL_SIGNS_UNITS,
        )
    elif input_format == "fhir":
        patient, all_disorders, all_vital_signs = extract_all_fhir(
            patient_id=PATIENT_ID,
            data_path=synthea_path,
            vital_signs_units=VITAL_SIGNS_UNITS,
        )
    else:
        print(f"{input_format} is not a valid format [csv, json, ccda, sql, fhir]")
        quit()

    print("\n\nSTEP 4 : Transform and Load compositions")
    transform_load(
        patient=patient,
        all_disorders=all_disorders,
        all_vital_signs=all_vital_signs,
        ehr_id=EHR_ID,
        output_path=composition_output_path,
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
