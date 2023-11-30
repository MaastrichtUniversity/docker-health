from pathlib import Path
import pandas as pd
from datetime import datetime

from contextlib import redirect_stdout
import io
import json
import yaml
from flatehr.cli import generate
from flatehr.cli.inspect_template import main as inspect



TEMPLATE_PATH = Path("data/templates")
SYNTHEA_PATH = Path("data/synthea/json")
CONF_PATH = Path("data/conf_files")


print("STEP 1: Generate a skeleton configuration yaml file")

# Patient template
template_file = TEMPLATE_PATH / "patient.json"
conf_skfile = CONF_PATH / "patient_skeleton_conf.yaml"
conf_file = CONF_PATH / "patient_conf.yaml"

skeleton_conf = io.StringIO()
with redirect_stdout(skeleton_conf):
    generate.skeleton(template_file)
with open(conf_skfile, "w") as file:
    print(skeleton_conf.getvalue(), file=file)


print("STEP 2: File the skeleton configuration yaml file based on template/data")

conf_dict_2 = {"ehr_id": {}, "paths": {}}


conf_dict_2["ehr_id"] = {"maps_to": [], "value": "{{ random_ehr_id() }}"}

conf_dict_2["paths"]["ctx/category|code"] = "433|event|"
  # 431|persistent| - of potential life-time validity;
  # 451|episodic| - valid over the life of a care episode;
  # 433|event| - valid at the time of recording (long-term validity requires subsequent clinical assessment).

conf_dict_2["paths"]["ctx/composer|id"] = "00000"
# conf_dict_2["paths"]["ctx/composer|id_scheme"] =
# conf_dict_2["paths"]["ctx/composer|id_namespace"] = 
conf_dict_2["paths"]["ctx/composer|name"] = "DataHub"

conf_dict_2["paths"]["ctx/encoding|code"] = "UTF-8"
conf_dict_2["paths"]["ctx/language"] = "en"
conf_dict_2["paths"]["ctx/territory"] = "nl"

# conf_dict_2["paths"]["ctx/setting|code"] = 
# conf_dict_2["paths"]["ctx/setting|value"] = 

conf_dict_2["paths"]["ctx/start_time"] = datetime.now().isoformat()

conf_dict_2["paths"]["ctx/subject|id"] = "$.attributes.id"
# conf_dict_2["paths"]["ctx/subject|id_scheme"] = 
# conf_dict_2["paths"]["ctx/subject|id_namespace"] = 
conf_dict_2["paths"]["ctx/subject|name"] = f"{'$.attributes.first_name'} {'$.attributes.last_name'}"

# https://jsonpath.com/
# conf_dict_2["paths"]["patient/birth/date_of_birth"]["maps_to"].append("$.attributes.birthdate_as_localdate")
conf_dict_2["paths"]["patient/birth/date_of_birth"] = {"maps_to": ["$.attributes.birthdate"]} # datetime.fromtimestamp(...) # remove last 3 digits 
# conf_dict_2["paths"]["patient/birth/date_of_birth"] = {"suffixes": {"|terminology": ["ISO_8601"]}}
conf_dict_2["paths"]["patient/death/date_of_death"] = {"maps_to": ["$.attributes.deathdate"]} # datetime.fromtimestamp(...) # remove last 3 digits 
# conf_dict_2["paths"]["patient/birth/date_of_death"] = {"suffixes": {"|terminology": ["ISO_8601"]}}
# conf_dict_2["paths"]["patient/gender/sex_assigned_at_birth|code"] = "$.attributes.gender"
conf_dict_2["paths"]["patient/gender/sex_assigned_at_birth"] = {"maps_to": ["$.attributes.gender"]}


with open(conf_file, 'w') as outfile:
    yaml.dump(conf_dict_2, outfile, default_flow_style=False)


print("STEP 3: Create a composition for a single patient")

input_file = SYNTHEA_PATH / "fc5b4365-670e-1d8b-b592-95a930c00c6c.json"


file = io.StringIO()
with redirect_stdout(file):
    generate.from_file(
        input_file,
        template_file=template_file,
        conf_file=conf_file,
        skip_ehr_id=False,
    )
stdout = file.getvalue()
# assert json.loads(stdout) == expected_composition
