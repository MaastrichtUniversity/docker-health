"""
Post the vital_signs.opt template
Create a unique EHR for a patient
Create a composition per encounter using a JSON composition as an example
Post the compositions
"""

import os
from pathlib import Path
import click

from src.etl import (
    extract_all_csv,
    extract_all_json,
    extract_all_ccda,
    extract_all_sql,
    extract_all_fhir,
    load_ehr_template,
    transform_post_compositions,
    test_versioning_functions,
)
from src.template import fetch_all_templates
from src.ehr import fetch_all_ehr_id


CONFIG = {
    "subject_id": "3b1dadde-eefe-e82a-efbc-daa3c959a0c2",
    "subject_namespace": "datahub",
    "template_filenames": [
        Path("data/templates/patient.opt"),
        Path("data/templates/diagnosis_demo.opt"),
        Path("data/templates/vital_signs.opt"),
    ],
    "vital_signs_units": {
        "Body Height": "cm",
        "Body Weight": "kg",
        "Heart rate": "/min",
        "Systolic Blood Pressure": "mm[Hg]",
        "Diastolic Blood Pressure": "mm[Hg]",
    },
    "write_composition": True,
}


@click.command(help="Runs all ETL for a single patient. [Accepted input_format: csv, sql, json, ccda, fhir]")
@click.argument("input_format")
def run(input_format):
    """Runs the ETL"""
    CONFIG["input_format"] = input_format
    CONFIG["synthea_path"] = Path(f"data/synthea/{CONFIG['input_format']}")

    print(f"\n\nEXTRACT data from {CONFIG['input_format']} input data format")
    if CONFIG["input_format"] == "csv":
        patient, all_disorders, all_vital_signs = extract_all_csv(
            subject_id=CONFIG["subject_id"],
            data_path=CONFIG["synthea_path"],
            vital_signs_units=CONFIG["vital_signs_units"],
        )
    elif CONFIG["input_format"] == "json":
        patient, all_disorders, all_vital_signs = extract_all_json(
            subject_id=CONFIG["subject_id"],
            data_path=CONFIG["synthea_path"],
            vital_signs_units=CONFIG["vital_signs_units"],
        )
    elif CONFIG["input_format"] == "ccda":
        patient, all_disorders, all_vital_signs = extract_all_ccda(
            subject_id=CONFIG["subject_id"],
            data_path=CONFIG["synthea_path"],
            vital_signs_units=CONFIG["vital_signs_units"],
        )
    elif CONFIG["input_format"] == "sql":
        patient, all_disorders, all_vital_signs = extract_all_sql(
            subject_id=CONFIG["subject_id"],
            data_path=CONFIG["synthea_path"],
            vital_signs_units=CONFIG["vital_signs_units"],
        )
    elif CONFIG["input_format"] == "fhir":
        patient, all_disorders, all_vital_signs = extract_all_fhir(
            subject_id=CONFIG["subject_id"],
            data_path=CONFIG["synthea_path"],
            vital_signs_units=CONFIG["vital_signs_units"],
        )
    else:
        print(f"{CONFIG['input_format']} is not a valid format [csv, json, ccda, sql, fhir]")
        quit()


    print("\n\nLOAD EHR and templates into the EHRbase")
    CONFIG["ehr_id"] = load_ehr_template(
        subject_id=CONFIG["subject_id"],
        template_filenames=CONFIG["template_filenames"],
    )


    print("\n\nTRANSFORM data classes into openEHR compositions and LOAD compositions")
    CONFIG["composition_output_path"] = Path("outputs/compositions") / CONFIG["subject_id"] / CONFIG["input_format"]
    os.makedirs(CONFIG["composition_output_path"], exist_ok=True)
    transform_post_compositions(
        patient=patient,
        all_disorders=all_disorders,
        all_vital_signs=all_vital_signs,
        ehr_id=CONFIG["ehr_id"],
        write_composition=CONFIG["write_composition"],
        output_path=CONFIG["composition_output_path"],
    )

    test_versioning_functions(
        subject_id=CONFIG["subject_id"],
        subject_namespace=CONFIG["subject_namespace"],
        patient=patient,
        write_composition=CONFIG["write_composition"],
        output_path=CONFIG["composition_output_path"],
    )

    # print("\n\nAnalysis")
    # plot_bloodpressure_over_time(ehr_id)


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


@click.group()
def cli():
    pass


cli.add_command(run)
cli.add_command(list_all_templates)
cli.add_command(get_all_ehr_id)

if __name__ == "__main__":
    cli()
