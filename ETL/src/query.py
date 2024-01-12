"""
Functions specific to AQL queries
"""

import json
from uuid import UUID

import requests

from src.diagnosis import Diagnosis
from src.ehr import EHRBASE_BASE_URL, EHRBASE_USERRNAME, EHRBASE_PASSWORD
from src.patient import Patient


def query_patient_composition(ehr_id: UUID, patient: Patient) -> bool:
    """
    Query the OpenEHR server to know if the patient data already exist in a composition.

    Parameters
    ----------
    ehr_id: UUID
        patient ehr_id to query
    patient: Patient
        Data object to check
    """
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = (
        f"SELECT c/uid/value as composition_uuid, "
        f"c/content[openEHR-EHR-EVALUATION.death_summary.v1]/data[at0001]/items[at0092]/null_flavour/value as dateOfDeath "
        f"FROM EHR e[ehr_id/value='{ehr_id}'] "
        f"CONTAINS COMPOSITION c "
        f"WHERE c/archetype_details/template_id/value='patient' "
        f"AND c/content[openEHR-EHR-EVALUATION.birth_summary.v0]/data[at0001]/items[at0004]/value/value='{patient.birth_date.isoformat()}' "
        f"AND c/content[openEHR-EHR-EVALUATION.gender.v1]/data[at0002]/items[at0019]/value/defining_code/code_string='{patient.gender_code}'"
    )
    # AND c/content[openEHR-EHR-EVALUATION.death_summary.v1]/data[at0001]/items[at0092]/null_flavour/value='{patient.death_date}'
    headers = {
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.request(
        "GET", url, headers=headers, params={"q": query}, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD), timeout=10
    )
    duplicate = False
    if response.status_code == 200:
        response_json = json.loads(response.text)
        # print(f"\nresponse_json: {json.dumps(response_json, indent=4)}")

        result = {
            "composition_uuid": response_json["rows"][0][0],
            "dateOfDeath": response_json["rows"][0][1],
        }
        # print(f"\nresult_json: {json.dumps(result, indent=4)}")

        if "composition_uuid" in result and result["dateOfDeath"] is None:
            print(f"DUPLICATE\tPatient composition data already exist with UUID: {result['composition_uuid']}'")
            duplicate = True

    return duplicate


def query_diagnosis_composition(ehr_id: UUID, diagnosis: Diagnosis) -> bool:
    """
    Query the OpenEHR server to know if the diagnosis data already exist in a composition.

    Parameters
    ----------
    ehr_id: UUID
        patient ehr_id to query
    diagnosis: Diagnosis
        Data object to check
    """
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = (
        f"SELECT c/uid/value as composition_uuid "
        f"FROM EHR e[ehr_id/value='{ehr_id}'] "
        f"CONTAINS COMPOSITION c "
        f"WHERE c/archetype_details/template_id/value='diagnosis_demo' "
        f"AND c/content[openEHR-EHR-EVALUATION.problem_diagnosis.v1]/data[at0001]/items[at0002]/value/defining_code/code_string='{diagnosis.snomed_code}' "
        f"AND c/content[openEHR-EHR-EVALUATION.problem_diagnosis.v1]/data[at0001]/items[at0002]/value/value='{diagnosis.description}' "
        f"AND c/content[openEHR-EHR-EVALUATION.problem_diagnosis.v1]/data[at0001]/items[at0003]/value/value='{diagnosis.start_date.strftime('%Y-%m-%dT%H:%M:%S')}' "
        f"AND c/content[openEHR-EHR-EVALUATION.problem_diagnosis.v1]/data[at0001]/items[at0030]/value/value='{diagnosis.stop_date.strftime('%Y-%m-%dT%H:%M:%S')}' "
    )
    headers = {
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.request(
        "GET", url, headers=headers, params={"q": query}, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD), timeout=10
    )
    duplicate = False
    if response.status_code == 200:
        response_json = json.loads(response.text)
        # print(f"\nresponse_json: {json.dumps(response_json, indent=4)}")

        if response_json["rows"]:
            print(f"DUPLICATE\tDiagnosis composition data already exist with UUID: {response_json['rows'][0]}'")
            duplicate = True

    return duplicate
