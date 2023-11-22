"""
Post the vital_signs.opt template
Create a unique EHR for a patient
Create a composition per encounter using a JSON composition as an example
Post the compositions
"""

from pathlib import Path
import pandas as pd
import click

from src.template import fetch_all_templates, post_template
from src.ehr import create_ehr, fetch_all_ehr_id
from src.composition import load_composition_example, update_composition_high_level, post_composition
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
    """This function is a proxy for the click command to interact with the above fetch_all_templates  function."""
    fetch_all_templates()


@click.command(help="Runs all ETL from default hard coded values")
def run():
    """Runs the ETL"""
    TEMPLATE_PATH = Path("data/template")
    COMPOSITION_PATH = Path("data/composition")
    SYNTHEA_PATH = Path("data/synthea_csv")

    EXAMPLE_COMPOSITION = "vital_signs_20231025075308_000001_1.json"
    PATIENT_ID = "a2f7ab19-64e1-6fb3-7232-413f04c55100"

    post_template(TEMPLATE_PATH / "vital_signs.opt")
    # list_all_templates()

    ehr_id = create_ehr(PATIENT_ID)
    # all_ehr_ids = get_all_ehr_id()

    observations = pd.read_csv(SYNTHEA_PATH / "observations.csv")
    encounters = pd.read_csv(SYNTHEA_PATH / "encounters.csv")

    patient_encounters = encounters.loc[encounters["PATIENT"] == PATIENT_ID]
    encounter_ids = patient_encounters["Id"].tolist()

    for encounter_id in encounter_ids:
        composition = load_composition_example(COMPOSITION_PATH / EXAMPLE_COMPOSITION)

        encounter_start = encounters.loc[encounters["Id"] == encounter_id]["START"].values[0]
        encounter_stop = encounters.loc[encounters["Id"] == encounter_id]["STOP"].values[0]

        composition = update_composition_high_level(composition, encounter_start, encounter_stop)

        if observations.loc[observations["ENCOUNTER"] == encounter_id].shape[0] == 0:
            print(f"{encounter_id} has no observations")
            continue

        vital_signs = observations[
            (observations["ENCOUNTER"] == encounter_id) & (observations["CATEGORY"] == "vital-signs")
        ]
        if vital_signs.shape[0] == 0:
            print(f"{encounter_id} has no vital signs observations")
            continue
        vital_signs_class = parse_vital_signs(vital_signs)
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
