from pathlib import Path
import pandas as pd
from datetime import datetime
from contextlib import redirect_stdout
import io
import json
import yaml
import ast
from flatehr.cli import generate
from flatehr.cli.inspect_template import main as inspect

from src.template import fetch_all_templates, post_template
from src.ehr import create_ehr, fetch_all_ehr_id
from src.composition import post_flat_composition

TEMPLATE_PATH = Path("data/templates")
SYNTHEA_PATH = Path("data/synthea/json")
CONF_PATH = Path("data/conf_files")

# Patient template
template_file = TEMPLATE_PATH / "patient.json"
conf_skfile = CONF_PATH / "patient_skeleton_conf.yaml"
conf_file = CONF_PATH / "patient_conf.yaml"


print(f"\nSTEP 1: Generate a skeleton configuration yaml file: {conf_skfile}")
# This step is only used to generated a skeleton of the configuration file from the web template

skeleton_conf = io.StringIO()
with redirect_stdout(skeleton_conf):
    generate.skeleton(template_file)
with open(conf_skfile, "w") as file:
    print(skeleton_conf.getvalue(), file=file)

with open(conf_skfile, "r") as file:
    print(file.read())
    # conf_dict = yaml.safe_load(file)
    # assert type(conf_dict) == dict


print(f"\nSTEP 2: Fill the skeleton configuration yaml file based on template/data: {conf_file}")
# A new dict is created with the required parameters described in the skeleton conf file
# The dict is filled with the fixed parameters and all paths should be written following JsonPath Syntax: https://jsonpath.com/
# These paths extract the data source and store them to a flat composition
# The dict is then dumped to a yaml file

# generate a random ehr identifier if necessary (can be off using the option skip_ehr_id=True in generate.from_file)
conf_dict = {
    "ehr_id": {"maps_to": [], "value": "{{ random_ehr_id() }}"},
    "paths": {}
}

# parameters linked to the data source:
conf_dict["paths"]["ctx/subject"] = {
    "maps_to": ["$.attributes.id", "$.attributes.first_name", "$.attributes.last_name"],
    "suffixes": {"|id": "{{ maps_to[0] }}", "|first_name": "{{ maps_to[1] }}", "|last_name": "{{ maps_to[2] }}"}
    # "|id_scheme", "|id_namespace"
}

conf_dict["paths"]["patient/birth/date_of_birth"] = {
    "maps_to": ["$.attributes.birthdate_as_localdate"],
    "suffixes": {"|date": "{{ maps_to[0] }}"}#, "|terminology": ["ISO_8601"]}
}
conf_dict["paths"]["patient/death/date_of_death"] = {
    "maps_to": ["$.attributes.deathdate"],
    "suffixes": {"|date": "{{ maps_to[0] }}"}#, "|terminology": ["ISO_8601"]}
} # datetime.fromtimestamp(...) # remove last 3 digits 

conf_dict["paths"]["patient/gender/sex_assigned_at_birth"] = {
    "maps_to": ["$.attributes.gender"],
    "suffixes": {"|code": "{{ maps_to[0] }}"}
}

# "fixed" hyper parameters:
conf_dict["paths"]["ctx/category|code"] = "433"
  # other codes:
  # 431|persistent| - of potential life-time validity;
  # 451|episodic| - valid over the life of a care episode;
  # 433|event| - valid at the time of recording (long-term validity requires subsequent clinical assessment).

conf_dict["paths"]["ctx/composer"] = {
    "maps_to": [],
    "suffixes": {
        "|name": "DataHub",
        # "|id": "???",
        # "|id_scheme": "???",
        # "|id_namespace": "???"
    }
} 

# conf_dict["paths"]["ctx/setting|code"] = ??
# conf_dict["paths"]["ctx/setting|value"] = ??

conf_dict["paths"]["ctx/encoding|code"] = "UTF-8"
conf_dict["paths"]["ctx/language"] = "en"
conf_dict["paths"]["ctx/territory"] = "nl"

conf_dict["paths"]["ctx/start_time"] = datetime.now().isoformat()


with open(conf_file, 'w') as outfile:
    yaml.dump(conf_dict, outfile, default_flow_style=False)

with open(conf_file, 'r') as file:
    print(file.read())


print("\nSTEP 3: Create a flat composition for a single patient")

patient_id = "fc5b4365-670e-1d8b-b592-95a930c00c6c"
input_file = SYNTHEA_PATH / f"{patient_id}.json"

file = io.StringIO()
with redirect_stdout(file):
    generate.from_file(
        input_file,
        template_file=template_file,
        conf_file=conf_file,
        skip_ehr_id=True,
    )
patient_flat_composition = ast.literal_eval(file.getvalue())
print(json.dumps(patient_flat_composition, indent = 4))
# assert json.loads(stdout) == expected_composition


print("\nSTEP 4: POST composition")

template_id = "patient"
post_template(TEMPLATE_PATH / f"{template_id}.opt")

ehr_id = create_ehr(patient_id)
# in composition.py, line "Accept": "application/json; charset=UTF-8" needed to be commented
# response = post_flat_composition(ehr_id, template_id, patient_flat_composition)


flat_composition = patient_flat_composition

url = f"{ECIS_BASE_URL}/composition/?format=FLAT&ehrId={ehr_id}&templateId={template_id}"

headers = {
    # "Accept": "application/json; charset=UTF-8",
    # "Prefer": "return=representation",
    "Content-Type": "application/json",
}
response = requests.request(
    "POST",
    url,
    headers=headers,
    data=json.dumps(flat_composition),
    auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
    timeout=10,
)

response_json = json.loads(response.text)
print(f"RESPONSE: {response.status_code}")
if response.ok:
    print(f"Composition was successfully created")
else:
    print(f'ERROR {response_json["error"]}')
    print(response_json["message"])
