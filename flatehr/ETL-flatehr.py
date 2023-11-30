from pathlib import Path
import pandas as pd
from datetime import datetime
from contextlib import redirect_stdout
import io
import json
import yaml
from flatehr.cli import generate
from flatehr.cli.inspect_template import main as inspect

from src.template import fetch_all_templates, post_template
from src.ehr import create_ehr, fetch_all_ehr_id
from src.composition import post_composition

TEMPLATE_PATH = Path("data/templates")
SYNTHEA_PATH = Path("data/synthea/json")
CONF_PATH = Path("data/conf_files")

# Patient template
template_file = TEMPLATE_PATH / "patient.json"
conf_skfile = CONF_PATH / "patient_skeleton_conf.yaml"
conf_file = CONF_PATH / "patient_conf.yaml"


print(f"STEP 1: Generate a skeleton configuration yaml file: {conf_skfile}")

skeleton_conf = io.StringIO()
with redirect_stdout(skeleton_conf):
    generate.skeleton(template_file)
with open(conf_skfile, "w") as file:
    print(skeleton_conf.getvalue(), file=file)

# with open(conf_skfile, "r") as file:
#     conf_dict = yaml.safe_load(file)
#     assert type(conf_dict) == dict


print(f"STEP 2: Fill the skeleton configuration yaml file based on template/data: {conf_file}")
# https://jsonpath.com/

conf_dict = {
    "ehr_id": {"maps_to": [], "value": "{{ random_ehr_id() }}"},
    "paths": {}
}

conf_dict["paths"]["ctx/category|code"] = "433|event|"
  # other codes:
  # 431|persistent| - of potential life-time validity;
  # 451|episodic| - valid over the life of a care episode;
  # 433|event| - valid at the time of recording (long-term validity requires subsequent clinical assessment).

conf_dict["paths"]["ctx/composer|name"] = "DataHub"
# conf_dict["paths"]["ctx/composer|id"] = ??
# conf_dict["paths"]["ctx/composer|id_scheme"] =??
# conf_dict["paths"]["ctx/composer|id_namespace"] = ??

# conf_dict["paths"]["ctx/setting|code"] = ??
# conf_dict["paths"]["ctx/setting|value"] = ??

conf_dict["paths"]["ctx/encoding|code"] = "UTF-8"
conf_dict["paths"]["ctx/language"] = "en"
conf_dict["paths"]["ctx/territory"] = "nl"


conf_dict["paths"]["ctx/start_time"] = datetime.now().isoformat()

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

with open(conf_file, 'w') as outfile:
    yaml.dump(conf_dict, outfile, default_flow_style=False)


print("STEP 3: Create a composition for a single patient")

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
patient_flat_composition = file.getvalue()
print("flat composition:")
print(patient_flat_composition)
with open(f"data/patient_flat_composition.json", "w") as file:
    print(patient_flat_composition, file=file)
# assert json.loads(stdout) == expected_composition



print("STEP 4: Create composition")

post_template(TEMPLATE_PATH / "patient.opt")
ehr_id = create_ehr(patient_id)

# need to convert flat composition to "normal" composition ..
reponse = post_composition(ehr_id, patient_flat_composition)
