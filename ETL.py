import json

import requests
import pandas as pd
import matplotlib.pyplot as plt

EHRBASE_USERRNAME = "ehrbase-user"
EHRBASE_PASSWORD = "SuperSecretPassword"
EHRBASE_BASE_URL = "http://localhost:8080/ehrbase/rest/openehr/v1"


def list_all_templates():
    url = f"{EHRBASE_BASE_URL}/definition/template/adl1.4"

    payload = {}
    headers = {
        "Accept": "application/json",
        "Prefer": "return=minimal",
    }

    response = requests.request("GET", url, headers=headers, data=payload, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD))

    print(response.text.encode("utf8"))


def get_all_ehr_id():
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = "SELECT e/ehr_id/value as ehr_id FROM EHR e"
    headers = {
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.request(
        "GET", url, headers=headers, params={"q": query}, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD)
    )
    response_json = json.loads(response.text)
    return response_json["rows"]


def get_bloodpressure_over_time(ehr_id):
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = f"SELECT c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/time as time,  c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0004]/value/magnitude as systolic ,  c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0005]/value/magnitude as diastolic FROM EHR e CONTAINS COMPOSITION c WHERE c/archetype_details/template_id/value='Vital signs' AND e/ehr_id/value='{ehr_id}'"
    headers = {
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.request(
        "GET", url, headers=headers, params={"q": query}, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD)
    )
    response_json = json.loads(response.text)
    df = pd.DataFrame(columns=["Time", "Systolic", "Diastolic"])

    for row in response_json["rows"]:
        df.loc[len(df)] = [row[0]["value"], row[1], row[2]]

    df["Time"] = pd.to_datetime(df["Time"])
    df = df.sort_values(by="Time")
    df.set_index("Time", inplace=True)
    df["Systolic"].plot()

    plt.show()


def post_template(filename):
    url = f"{EHRBASE_BASE_URL}/definition/template/adl1.4"

    payload = open(filename, "rb").read()

    headers = {"Accept": "application/xml", "Prefer": "return=minimal", "Content-Type": "application/xml"}

    response = requests.request("POST", url, headers=headers, data=payload, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD))

    if response.ok:
        print(f"Template {filename} successfully added")


def create_ehr(patient_id):

    ehr_id = get_ehr_id_for_subject_id(patient_id)
    if ehr_id:
        return ehr_id

    url = f"{EHRBASE_BASE_URL}/ehr"
    id_payload = {
        "_type": "EHR_STATUS",
        "archetype_node_id": "openEHR-EHR-EHR_STATUS.generic.v1",
        "name": {"value": "EHR Status"},
        "subject": {
            "external_ref": {
                "id": {"_type": "GENERIC_ID", "value": patient_id, "scheme": "datahub"},
                "namespace": "datahub",
                "type": "PERSON",
            }
        },
        "is_modifiable": True,
        "is_queryable": True,
    }

    headers = {"Accept": "application/json", "Prefer": "return=representation", "Content-Type": "application/json"}
    response = requests.request(
        "POST", url, data=json.dumps(id_payload), headers=headers, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD)
    )
    response_json = json.loads(response.text)

    return response_json["ehr_id"]["value"]


def get_ehr_id_for_subject_id(subject_id):

    url = f"{EHRBASE_BASE_URL}/ehr"
    myparams = {"subject_id": subject_id, "subject_namespace": "datahub"}
    headers = {
        "Accept": "application/json",
        "Prefer": "return=minimal",
    }

    response = requests.request(
        "GET", url, headers=headers, params=myparams, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD)
    )

    if response.status_code == 404:
        return ""

    response_json = json.loads(response.text)
    return response_json["ehr_id"]["value"]


def load_composition_example(filename):
    file = open(filename, "rb")
    return json.load(file)


def post_composition(ehr_id, composition):
    print(json.dumps(composition))

    url = f"{EHRBASE_BASE_URL}/ehr/{ehr_id}/composition"
    headers = {
        "Accept": "application/json; charset=UTF-8",
        "Prefer": "return=representation",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(composition), auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD)
    )
    response_json = json.loads(response.text)

    return response_json["uid"]["value"]


def update_composition_high_level(composition, start_time, end_time):
    # set territory
    composition["territory"]["code_string"] = "NL"
    # set composer
    composition["composer"]["name"] = "DataHub"
    # set start time
    composition["context"]["start_time"]["value"] = start_time
    composition["context"]["end_time"] = {"value": end_time}
    return composition


def update_composition_vital_signs(composition, vital_signs):

    systolic = vital_signs[vital_signs["DESCRIPTION"] == "Systolic Blood Pressure"]["VALUE"].values[0]
    diastolic = vital_signs[vital_signs["DESCRIPTION"] == "Diastolic Blood Pressure"]["VALUE"].values[0]
    time = vital_signs[vital_signs["DESCRIPTION"] == "Systolic Blood Pressure"]["DATE"].values[0]
    bmi = vital_signs[vital_signs["DESCRIPTION"] == "Body mass index (BMI) [Ratio]"]["VALUE"].values[0]
    height = vital_signs[vital_signs["DESCRIPTION"] == "Body Height"]["VALUE"].values[0]
    weight = vital_signs[vital_signs["DESCRIPTION"] == "Body Weight"]["VALUE"].values[0]
    heart_rate = vital_signs[vital_signs["DESCRIPTION"] == "Heart rate"]["VALUE"].values[0]
    respiration_rate = vital_signs[vital_signs["DESCRIPTION"] == "Respiratory rate"]["VALUE"].values[0]

    for index, item in enumerate(composition["content"]):
        # Update bloodpressure
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.blood_pressure.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = systolic
            composition["content"][index]["data"]["events"][0]["data"]["items"][1]["value"]["magnitude"] = diastolic
        # update BMI
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.body_mass_index.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = bmi
        # Update height
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.height.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = height
        # Update weight
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.body_weight.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = weight

        # Update heart rate
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.pulse.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"] = heart_rate

        # Update respiration rate
        if item["archetype_details"]["archetype_id"]["value"] == "openEHR-EHR-OBSERVATION.respiration.v2":
            composition["content"][index]["data"]["origin"]["value"] = time
            composition["content"][index]["data"]["events"][0]["time"]["value"] = time
            # Hard coded the order
            composition["content"][index]["data"]["events"][0]["data"]["items"][0]["value"][
                "magnitude"
            ] = respiration_rate

    return composition


# all_ehr_ids = get_all_ehr_id()
# list_all_templates()
post_template("vital_signs.opt")
# list_all_templates()


patient_id = "a2f7ab19-64e1-6fb3-7232-413f04c55100"

ehr_id = create_ehr(patient_id)

observations = pd.read_csv("synthea_csv/observations.csv")
encounters = pd.read_csv("synthea_csv/encounters.csv")

patient_encounters = encounters.loc[encounters["PATIENT"] == patient_id]
encounter_ids = patient_encounters["Id"].tolist()

for encounter_id in encounter_ids:
    composition = load_composition_example("vital_signs_20231025075308_000001_1.json")

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

    composition = update_composition_vital_signs(composition, vital_signs)
    post_composition(ehr_id, composition)

get_bloodpressure_over_time(ehr_id)
