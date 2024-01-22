"""
Functions specific to AQL queries
"""

import json
from uuid import UUID
import requests

from src.ehr import EHRBASE_BASE_URL, EHRBASE_USERRNAME, EHRBASE_PASSWORD
from src.patient import Patient
from src.diagnosis import Diagnosis
from src.vitalsigns import VitalSigns


def retrieve_all_compositions_from_ehr(ehr_id: UUID) -> list:
    """
    Retrieve all compositions stored for a unique ehr_id and return a list of all compositions
    containing the template_id, start_time and the latest versioned_composition_id

    Parameters
    ----------
    ehr_id: UUID
        ehr_id of the given patient

    Returns
    -------
    list
        List of retrieved compositions for this ehr_id. List ordered by start_time values
        For each composition, the template_id, start_time and versioned_composition_id are returned
    """
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = (
        f"SELECT c/name/value, c/context/start_time/value, c/uid/value  "
        f"FROM EHR e[ehr_id/value='{ehr_id}'] "
        f"CONTAINS COMPOSITION c "
        f"ORDER BY c/context/start_time/value ASC"
    )
    headers = {
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.request(
        method="GET",
        url=url,
        headers=headers,
        params={"q": query},
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )

    response_json = json.loads(response.text)

    if response.ok:
        return response_json["rows"]
    print("No posted compositions for this patient")
    return None


def check_duplicate_patient_composition(ehr_id: UUID, patient: Patient) -> bool:
    """
    Query the OpenEHR server to know if the given patient data already exist in a composition.

    Parameters
    ----------
    ehr_id: UUID
        patient ehr_id to query
    patient: Patient
        Instance of the Patient object

    Returns
    -------
    bool
        Boolean value, if true the composition is duplicated for this ehr_id and given Patient data
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
        method="GET",
        url=url,
        headers=headers,
        params={"q": query},
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    duplicate = False
    if response.status_code == 200:
        response_json = json.loads(response.text)
        # print(f"\nresponse_json: {json.dumps(response_json, indent=4)}")

        result = {
            "composition_uuid": response_json["rows"][0][0],
            "dateOfDeath": response_json["rows"][0][1],
        }
        if "composition_uuid" in result and result["dateOfDeath"] is None:
            print(
                f"DUPLICATE\tComposition found for this specific ehr_id and the given data with UUID: "
                f"{result['composition_uuid']}'"
            )
            duplicate = True

    return duplicate


def check_duplicate_diagnosis_composition(ehr_id: UUID, diagnosis: Diagnosis) -> bool:
    """
    Query the OpenEHR server to know if the given diagnosis data already exist in a composition.

    Parameters
    ----------
    ehr_id: UUID
        patient ehr_id to query
    diagnosis: Diagnosis
        Instance of the Diagnosis object

    Returns
    -------
    bool
        Boolean value, if true the composition is duplicated for this ehr_id and given Diagnosis data
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
        method="GET",
        url=url,
        headers=headers,
        params={"q": query},
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    duplicate = False
    if response.status_code == 200:
        response_json = json.loads(response.text)
        # print(f"\nresponse_json: {json.dumps(response_json, indent=4)}")

        if response_json["rows"]:
            print(
                f"DUPLICATE\tComposition found for this specific ehr_id and the given data with UUID: "
                f"{response_json['rows'][0][0]}'"
            )
            duplicate = True

    return duplicate


def check_duplicate_vital_signs_composition(ehr_id: UUID, vital_signs: VitalSigns) -> bool:
    """
    Query the OpenEHR server to know if the given vital signs data already exist in a composition.

    Parameters
    ----------
    ehr_id: UUID
        patient ehr_id to query
    vital_signs: VitalSigns
        Instance of the VitalSigns object

    Returns
    -------
    bool
        Boolean value, if true the composition is duplicated for this ehr_id and given VitalSigns data
    """
    url = f"{EHRBASE_BASE_URL}/query/aql"
    query = (
        f"SELECT c/uid/value as composition_uuid, "
        f"c/content[openEHR-EHR-OBSERVATION.body_weight.v2]/data[at0002]/events[at0003]/data[at0001]/items[at0004]/value/magnitude as weight, "
        f"c/content[openEHR-EHR-OBSERVATION.height.v2]/data[at0001]/events[at0002]/data[at0003]/items[at0004]/value/magnitude as height, "
        f"c/content[openEHR-EHR-OBSERVATION.pulse.v2]/data[at0002]/events[at0003]/data[at0001]/items[at0004]/value/magnitude as heart, "
        f"c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0004]/value/magnitude as systolic, "
        f"c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0005]/value/magnitude as diastolic "
        f"FROM EHR e[ehr_id/value='{ehr_id}'] "
        f"CONTAINS COMPOSITION c "
        f"WHERE c/archetype_details/template_id/value='vital_signs' "
        f"AND c/content[openEHR-EHR-OBSERVATION.height.v2]/data[at0001]/events[at0002]/data[at0003]/items[at0004]/value/magnitude={vital_signs.height.measurements[0].value}"
        f"AND c/content[openEHR-EHR-OBSERVATION.body_weight.v2]/data[at0002]/events[at0003]/data[at0001]/items[at0004]/value/magnitude={vital_signs.weight.measurements[0].value} "
        f"AND c/content[openEHR-EHR-OBSERVATION.pulse.v2]/data[at0002]/events[at0003]/data[at0001]/items[at0004]/value/magnitude={vital_signs.heart_rate.measurements[0].value} "
        f"AND c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0004]/value/magnitude={vital_signs.blood_systolic.measurements[0].value} "
        f"AND c/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]/data[at0001]/events[at0006]/data[at0003]/items[at0005]/value/magnitude={vital_signs.blood_diastolic.measurements[0].value}"
    )
    headers = {
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    response = requests.request(
        method="GET",
        url=url,
        headers=headers,
        params={"q": query},
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10,
    )
    duplicate = False
    if response.status_code == 200:
        response_json = json.loads(response.text)
        # print(f"\nresponse_json: {json.dumps(response_json, indent=4)}")

        if response_json["rows"]:
            print(
                f"DUPLICATE\tComposition found for this specific ehr_id and the given data with UUID: "
                f"{response_json['rows'][0][0]}'"
            )
            duplicate = True

    return duplicate
