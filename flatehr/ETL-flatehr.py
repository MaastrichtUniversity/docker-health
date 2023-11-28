from pathlib import Path
import pandas as pd

from contextlib import redirect_stdout
import io
import json
import yaml
from flatehr.cli import generate
from flatehr.cli.inspect_template import main as inspect



TEMPLATE_PATH = Path("data/templates")
SYNTHEA_PATH = Path("data/synthea_csv")
CONF_PATH = Path("data/conf_files")


print("STEP 1: Generate a configuration yaml file for each web template")

# Patient template
template_file = TEMPLATE_PATH / "patient.json"
conf_file = CONF_PATH / "patient_conf.yaml"

skeleton_conf = io.StringIO()
with redirect_stdout(skeleton_conf):
    generate.skeleton(template_file)
with open(conf_file, "w") as file:
    print(skeleton_conf.getvalue(), file=file)

with open(conf_file, "r") as file:
    conf_dict = yaml.safe_load(file)
    assert type(conf_dict) == dict


conf_dict["paths"]["ctx/category|code"] = "433|event|"
  # 431|persistent| - of potential life-time validity;
  # 451|episodic| - valid over the life of a care episode;
  # 433|event| - valid at the time of recording (long-term validity requires subsequent clinical assessment).

conf_dict["paths"]["ctx/composer|id"] = "00000"
# conf_dict["paths"]["ctx/composer|id_scheme"] =
# conf_dict["paths"]["ctx/composer|id_namespace"] = 
conf_dict["paths"]["ctx/composer|name"] = "DataHub"

conf_dict["paths"]["ctx/encoding|code"] = "UTF-8"
conf_dict["paths"]["ctx/language"] = "en"
conf_dict["paths"]["ctx/territory"] = "nl"

# conf_dict["paths"]["ctx/setting|code"] = 
# conf_dict["paths"]["ctx/setting|value"] = 

conf_dict["paths"]["ctx/start_time"] = datetime.now().isoformat()

conf_dict["paths"]["ctx/subject|id"] = "$.attributes.id"
# conf_dict["paths"]["ctx/subject|id_scheme"] = 
# conf_dict["paths"]["ctx/subject|id_namespace"] = 
conf_dict["paths"]["ctx/subject|name"] = f"{'$.attributes.first_name'} {'$.attributes.last_name'}"

# https://jsonpath.com/
# conf_dict["paths"]["patient/birth/date_of_birth"]["maps_to"].append("$.attributes.birthdate_as_localdate")
conf_dict["paths"]["patient/birth/date_of_birth"]["maps_to"].append("$.attributes.birthdate") # datetime.fromtimestamp(...) # remove last 3 digits 
# conf_dict["paths"]["patient/birth/date_of_birth"]["suffixes"]["|terminology"].append("ISO_8601")
conf_dict["paths"]["patient/death/date_of_death"]["maps_to"].append("$.attributes.deathdate") # datetime.fromtimestamp(...) # remove last 3 digits 
# conf_dict["paths"]["patient/birth/date_of_death"]["suffixes"]["|terminology"].append("ISO_8601")
conf_dict["paths"]["patient/gender/sex_assigned_at_birth|code"] = "$.attributes.gender"


with open("test.yaml", 'w') as outfile:
    yaml.dump(conf_dict, outfile, default_flow_style=False)


f = io.StringIO()
with redirect_stdout(f):
    generate.from_file(
        input_file,
        template_file=template_file,
        conf_file=conf_file,
        skip_ehr_id=True,
    )
stdout = file.getvalue()
# assert json.loads(stdout) == expected_composition
