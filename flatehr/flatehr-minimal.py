"""
Example of posting a composition using the flatehr package and JSONpath Synthax.
Minimal configuration file.
"""


import io
from pathlib import Path
import json
import ast
from contextlib import redirect_stdout
import yaml
from flatehr.cli import generate
from flatehr.cli.inspect_template import main as inspect

from src.template import post_template
from src.ehr import create_ehr
from src.composition import post_flat_composition_2

TEMPLATE_PATH = Path("data/templates")
SYNTHEA_PATH = Path("data/synthea/json")
CONF_PATH = Path("data/conf_files")
TEMPLATE_ID = "patient"
PATIENT_ID = "fc5b4365-670e-1d8b-b592-95a930c00c6c"

if __name__ == "__main__":

    # Patient template
    web_template_filename = TEMPLATE_PATH / f"{TEMPLATE_ID}.json"
    odt_template_filename = TEMPLATE_PATH / f"{TEMPLATE_ID}.opt"
    conf_skfilename = CONF_PATH / f"{TEMPLATE_ID}_skeleton_conf.yaml"
    conf_filename = CONF_PATH / f"{TEMPLATE_ID}_conf_minimal.yaml"


    print(f"\nSTEP 1: Generate a skeleton configuration yaml file: {conf_skfilename}")
    # This step is only used to generated a skeleton of the configuration file from the web template

    skeleton_conf = io.StringIO()
    with redirect_stdout(skeleton_conf):
        generate.skeleton(web_template_filename)
    with open(conf_skfilename, "w", encoding="utf-8") as file:
        print(skeleton_conf.getvalue(), file=file)

    with open(conf_skfilename, "r", encoding="utf-8") as file:
        print(file.read())


    print(f"\nSTEP 2: Fill the skeleton configuration yaml file based on template/data: {conf_filename}")
    # A new dict is created with the required parameters described in the skeleton conf file
    # The dict is filled with the fixed parameters and all paths should be written following
    # JsonPath Syntax: https://jsonpath.com/
    # These paths extract the data source and store them to a flat composition
    # The dict is then dumped to a yaml file

    # generate a random ehr identifier if necessary (can be off using the option skip_ehr_id=True in generate.from_file)
    conf_dict = {
        "ehr_id": {"maps_to": [], "value": "{{ random_ehr_id() }}"},
        "paths": {}
    }
    ## parameters linked to the data source:
    conf_dict["paths"]["patient/birth/date_of_birth"] = {
        "maps_to": ["$.attributes.birthdate_as_localdate"],
        "suffixes": {"": "{{ maps_to[0] }}"}
    }
    conf_dict["paths"]["patient/death/date_of_death"] = {
        "maps_to": ["$.attributes.deathdate"],
        "suffixes": {"": "{{ maps_to[0] }}"}
    }
    conf_dict["paths"]["patient/gender/sex_assigned_at_birth"] = {
        "maps_to": ["$.attributes.gender"],
        "suffixes": {"|code": "{{ maps_to[0] }}"}
    }

    ## "fixed" hyper parameters:
    conf_dict["paths"]["patient/territory"] = {
        "suffixes": {
            "|code": "NL",
            "|terminology": "ISO_3166-1"
        }
    }
    conf_dict["paths"]["patient/composer"] = {
        "suffixes": {
            "|name": "DataHub",
        }
    }

    with open(conf_filename, 'w', encoding="utf-8") as outfile:
        yaml.dump(conf_dict, outfile, default_flow_style=False)

    with open(conf_filename, 'r', encoding="utf-8") as file:
        print(file.read())


    print("\nSTEP 3: Create a flat composition for a single patient")

    data_filename = SYNTHEA_PATH / f"{PATIENT_ID}.json"

    file = io.StringIO()
    with redirect_stdout(file):
        generate.from_file(
            data_filename,
            template_file=web_template_filename,
            conf_file=conf_filename,
            skip_ehr_id=True,
        )
    patient_flat_composition = ast.literal_eval(file.getvalue())
    print(json.dumps(patient_flat_composition, indent = 4))
    # assert json.loads(stdout) == expected_composition


    print("\nSTEP 4: POST composition")

    post_template(odt_template_filename)
    ehr_id = create_ehr(PATIENT_ID)
    patient_flat_composition = ast.literal_eval(file.getvalue())
    response = post_flat_composition_2(ehr_id, TEMPLATE_ID, patient_flat_composition)
