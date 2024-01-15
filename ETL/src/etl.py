"""
Functions to extract demo data from various input formats.
Create object instances for single patient: Patient, Diagnosis and VitalSigns.
Transform each data instance into a composition.
Load each composition to the EHRbase server.
"""

import re
import json
import sqlite3
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd

from src.composition import (
    transform_composition,
    post_composition,
    write_json_composition,
    update_composition,
    delete_composition,
    get_all_versioned_composition_uuids,
    get_composition_at_version
)

from src.patient import (
    Patient,
    parse_patient_csv,
    parse_patient_json,
    parse_patient_ccda,
    parse_patient_sql,
    create_patient_instance,
    parse_patient_fhir,
)
from src.diagnosis import (
    Diagnosis,
    parse_all_diagnosis_csv,
    parse_all_diagnosis_json,
    parse_all_diagnosis_ccda,
    get_all_diagnosis_sql,
    parse_diagnosis_sql,
    create_diagnosis_instance,
    parse_diagnosis_fhir,
)
from src.vitalsigns import (
    VitalSigns,
    parse_vital_signs_csv,
    parse_vital_signs_json,
    parse_vital_signs_ccda,
    get_all_vital_signs_sql,
    parse_all_vital_signs_sql,
    create_vital_signs_instance,
    parse_all_vital_signs_fhir,
)
from src.query import (
    retireve_all_compositions_from_ehr
)



def extract_all_csv(patient_id, data_path, vital_signs_units) -> (Patient, list[Diagnosis], list[VitalSigns]):
    """
    Extract the values on a patient, its diagnosis and vital signs from the CSV files

    Parameters
    ----------
    patient_id: str
        External patient id
    data_path: str
        Path to the CSV files
    vital_signs_units: dict
        Dictionary containing as keys all the vital signs variables used,
        and as values the corresponding chosen units

    Returns
    -------
    Patient
        Instance of the Patient class
    list[Diagnosis]
        list of instances of the Diagnosis class
    list[VitalSigns]
        list of instances of the VitalSigns class
    """
    # Load datasets
    patients_df = pd.read_csv(data_path / "patients.csv")
    conditions_df = pd.read_csv(data_path / "conditions.csv")
    observations_df = pd.read_csv(data_path / "observations.csv")
    encounters_df = pd.read_csv(data_path / "encounters.csv")
    # all_encounters = parse_all_encounters(encounters_df)

    print("\nPatient..", end="\t")
    patient_df = patients_df[patients_df["Id"] == patient_id]
    patient = create_patient_instance(*parse_patient_csv(patient_df))
    print(f"information extracted for patient_id: {patient_id}")

    print("\nDiagnosis..", end="\t")
    where_disorder = conditions_df["DESCRIPTION"].apply(lambda x: bool(re.search(".*(disorder)", x)))
    patient_disorders_df = conditions_df[where_disorder].query("PATIENT == @patient_id")
    all_disorders = []
    for _, disorder_df in patient_disorders_df.iterrows():
        all_disorders.append(create_diagnosis_instance(*parse_all_diagnosis_csv(disorder_df)))
    print(f"{len(all_disorders)} disorders reported for this patient.")

    print("\nVital Signs..", end="\t")
    patient_encounter_ids = encounters_df[encounters_df["PATIENT"] == patient_id]["Id"].tolist()
    vital_signs_df = observations_df[
        (observations_df["ENCOUNTER"].isin(patient_encounter_ids))
        & (observations_df["CATEGORY"] == "vital-signs")
        # (observations_df['DESCRIPTION'].isin(VITAL_SIGNS_UNITS.keys()))
    ]

    all_vital_signs = []
    for encounter_id in patient_encounter_ids:
        vital_signs_enc_df = vital_signs_df[vital_signs_df["ENCOUNTER"] == encounter_id]
        if vital_signs_enc_df.shape[0] == 0:
            # print(f"Encounter id {encounter_id} has no vital signs observations")
            continue

        all_vital_signs.append(
            create_vital_signs_instance(
                parse_vital_signs_csv(vital_signs_enc_df),
                vital_signs_units,
            )
        )
    print(f"{len(all_vital_signs)} vital signs reported for this patient.")

    return patient, all_disorders, all_vital_signs


def extract_all_json(patient_id, data_path, vital_signs_units) -> (Patient, list[Diagnosis], list[VitalSigns]):
    """
    Extract the values on a patient, its diagnosis and vital signs from a single JSON patient file

    Parameters
    ----------
    patient_id: str
        External patient id
    data_path: str
        Path to the JSON patient file
    vital_signs_units: dict
        Dictionary containing as keys all the vital signs variables used,
        and as values the corresponding chosen units

    Returns
    -------
    Patient
        Instance of the Patient class
    list[Diagnosis]
        list of instances of the Diagnosis class
    list[VitalSigns]
        list of instances of the VitalSigns class
    """
    # Load json patient file as a python dictionary
    with open(data_path / f"{patient_id}.json", encoding="utf-8") as infile:
        patient_json = json.load(infile)

    print("\nPatient..", end="\t")
    patient = create_patient_instance(*parse_patient_json(patient_json))
    print(f"information extracted for patient_id: {patient_id}")

    print("\nDiagnosis..", end="\t")
    all_disorders = []
    for encounter_i, encounter in enumerate(patient_json["record"]["encounters"]):
        if "conditions" in encounter:
            for condition_j, condition in enumerate(encounter["conditions"]):
                description = condition["codes"][0]["display"]
                if not bool(re.search(".*(disorder)", description)):
                    # print("Current condition is not classified as a disorder.")
                    continue
                all_disorders.append(
                    create_diagnosis_instance(*parse_all_diagnosis_json(patient_json, encounter_i, condition_j))
                )
    print(f"{len(all_disorders)} disorders reported for this patient.")

    print("\nVital Signs..")
    all_vital_signs = []
    for encounter_i, encounter in enumerate(patient_json["record"]["encounters"]):
        if encounter["observations"] == []:
            # print(f"Encounter id {encounter_i} has no vital signs observations")
            continue
        list_observations_j = []
        for observation_j, observation in enumerate(encounter["observations"]):
            if observation["category"] == "vital-signs":
                list_observations_j.append(observation_j)

        all_vital_signs.append(
            create_vital_signs_instance(
                parse_vital_signs_json(patient_json, encounter_i, list_observations_j),
                vital_signs_units,
            )
        )
    print(f"{len(all_vital_signs)} vital signs reported for this patient.")

    return patient, all_disorders, all_vital_signs


def extract_all_ccda(patient_id, data_path, vital_signs_units) -> (Patient, list[Diagnosis], list[VitalSigns]):
    """
    Extract the values on a patient, its diagnosis and vital signs from the CCDA XML files

    Parameters
    ----------
    patient_id: str
        External patient id
    data_path: str
        Path to the CDDA patient file
    vital_signs_units: dict
        Dictionary containing as keys all the vital signs variables used,
        and as values the corresponding chosen units

    Returns
    -------
    Patient
        Instance of the Patient class
    list[Diagnosis]
        list of instances of the Diagnosis class
    list[VitalSigns]
        list of instances of the VitalSigns class
    """
    # Parse patient xml file
    tree = ET.parse(f"{data_path}/{patient_id}.xml")
    # tree = ET.parse(f"/home/daniel/datahub/openEHR/docker-health/demo_data/ccda/{patient_id}.xml")
    patient_xml = tree.getroot()

    print("\nPatient..", end="\t")
    patient = create_patient_instance(*parse_patient_ccda(patient_xml))
    print(f"information extracted for patient_id: {patient_id}")

    print("\nDiagnosis..", end="\t")
    all_disorders = []

    entries = patient_xml.findall(".//{urn:hl7-org:v3}code[@code='11450-4'].../{urn:hl7-org:v3}entry")
    for entry in entries:
        observation = entry.find(
            "./{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}value"
        ).attrib["displayName"]
        if not bool(re.search(".*(disorder)", observation)):
            continue
        all_disorders.append(create_diagnosis_instance(*parse_all_diagnosis_ccda(entry)))
    print(f"{len(all_disorders)} disorders reported for this patient.")

    # In ccda vital sign are not clustered together.
    # Only way to get some clustering is on date

    print("\nVital Signs..", end="\t")
    all_vital_signs = []

    # get all unique dates for vital signs observations
    observation_dates = []
    observations = patient_xml.findall(
        ".//{urn:hl7-org:v3}organizer/{urn:hl7-org:v3}code[@code='46680005']...//{urn:hl7-org:v3}observation/{urn:hl7-org:v3}effectiveTime"
    )
    for observation in observations:
        observation_dates.append(observation.attrib["value"])
    observation_dates = list(set(observation_dates))

    for observation_date in observation_dates:
        observations_on_specific_date = patient_xml.findall(
            f".//{{urn:hl7-org:v3}}organizer/{{urn:hl7-org:v3}}code[@code='46680005']...//{{urn:hl7-org:v3}}observation/{{urn:hl7-org:v3}}effectiveTime[@value='{observation_date}']..."
        )
        all_vital_signs.append(
            create_vital_signs_instance(
                parse_vital_signs_ccda(observations_on_specific_date),
                vital_signs_units,
            )
        )

    print(f"{len(all_vital_signs)} vital signs reported for this patient.")

    return patient, all_disorders, all_vital_signs


def extract_all_sql(patient_id, data_path, vital_signs_units) -> (Patient, list[Diagnosis], list[VitalSigns]):
    """
    Extract the values on a patient, its diagnosis and vital signs from the SQL files

    Parameters
    ----------
    patient_id: str
        External patient id
    data_path: str
        Path to the SQL files
    vital_signs_units: dict
        Dictionary containing as keys all the vital signs variables used,
        and as values the corresponding chosen units

    Returns
    -------
    Patient
        Instance of the Patient class
    list[Diagnosis]
        list of instances of the Diagnosis class
    list[VitalSigns]
        list of instances of the VitalSigns class
    """
    print("\nPatient..", end="\t")
    connection = sqlite3.connect(data_path / "patients.sqlite")
    patient = create_patient_instance(*parse_patient_sql(connection, patient_id))
    connection.close()
    print(f"information extracted for patient_id: {patient_id}")

    print("\nDiagnosis...", end="\t")
    connection = sqlite3.connect(data_path / "conditions.sqlite")
    patient_diagnosis_sql = get_all_diagnosis_sql(connection, patient_id)
    all_disorders = []
    for diagnosis in patient_diagnosis_sql:
        all_disorders.append(create_diagnosis_instance(*parse_diagnosis_sql(diagnosis)))
    connection.close()
    print(f"{len(all_disorders)} disorders reported for this patient.")

    print("\nVital Signs..", end="\t")
    connection = sqlite3.connect(data_path / "observations.sqlite")
    vital_signs_unparsed = get_all_vital_signs_sql(connection, patient_id)
    encounter_ids, inds = np.unique(vital_signs_unparsed["encounter_id"], return_index=True)
    encounter_ids = encounter_ids[np.argsort(inds)]
    all_vital_signs = []
    for encounter_id in encounter_ids:
        vital_signs_enc_df = vital_signs_unparsed[vital_signs_unparsed["encounter_id"] == encounter_id]
        vital_signs = create_vital_signs_instance(parse_all_vital_signs_sql(vital_signs_enc_df), vital_signs_units)
        all_vital_signs.append(vital_signs)
    connection.close()
    print(f"{len(all_vital_signs)} vital signs reported for this patient.")

    return patient, all_disorders, all_vital_signs


def extract_all_fhir(patient_id, data_path, vital_signs_units) -> (Patient, list[Diagnosis], list[VitalSigns]):
    """
    Extract the values on a patient, its diagnosis and vital signs from a single fhir JSON patient file

    Parameters
    ----------
    patient_id: str
        External patient id
    data_path: str
        Path to the fhir JSON patient file
    vital_signs_units: dict
        Dictionary containing as keys all the vital signs variables used,
        and as values the corresponding chosen units

    Returns
    -------
    Patient
        Instance of the Patient class
    list[Diagnosis]
        list of instances of the Diagnosis class
    list[VitalSigns]
        list of instances of the VitalSigns class
    """
    # Load json patient file as a python dictionary
    with open(f"{data_path}/{patient_id}.json", encoding="utf-8") as infile:
        patient_json = json.load(infile)

    print("\nPatient..", end="\t")

    patient = parse_patient_fhir(patient_json)
    print(f"information extracted for patient_id: {patient_id}")

    print("\nDiagnosis..", end="\t")
    all_disorders = []
    encounters = {}
    for entry in patient_json["entry"]:
        if "Condition" in entry["resource"]["resourceType"]:
            description = entry["resource"]["code"]["text"]
            if not bool(re.search(".*(disorder)", description)):
                # print("Current condition is not classified as a disorder.")
                continue
            all_disorders.append(parse_diagnosis_fhir(entry["resource"]))

        if "Observation" in entry["resource"]["resourceType"]:
            observation = entry["resource"]
            if observation["category"][0]["coding"][0]["code"] == "vital-signs":
                encounter_id = observation["encounter"]["reference"]
                if encounter_id not in encounters:
                    encounters[encounter_id] = [observation]
                else:
                    encounters[encounter_id].append(observation)

    print(f"{len(all_disorders)} disorders reported for this patient.")

    print("\nVital Signs..")
    all_vital_signs = []
    for observations in encounters.values():
        all_vital_signs.append(parse_all_vital_signs_fhir(observations, vital_signs_units))

    return patient, all_disorders, all_vital_signs


def switch_patient_sex(patient, ehr_id, patient_composition_id, output_path):
    """
    Switch the sex assigned at birth of the patient.

    Parameters
    ----------
    patient: Patient
        Instance of the Patient class
    ehr_id: UUID
        ehr_id for the given patient id
    patient_composition_id: UUID
        Composition UUID, containing the host and version (UUID::host::version)
    output_path: str
        Path the the folder saving all composition outputs

    Returns
    -------
    UUID
        New patient composition UUID
    """
    if patient.gender_code == "M":
        patient.gender_code = "F"
    elif patient.gender_code == "F":
        patient.gender_code = "M"

    simplified_patient_composition = patient.model_dump_json(by_alias=True, indent=4)
    print(f"patient: {simplified_patient_composition}")
    patient_composition = transform_composition(
        simplified_composition=simplified_patient_composition,
        template_id="patient",
    )
    # print(f"\ncomposition: {patient_composition}")
    write_json_composition(
        composition=patient_composition,
        json_filename=output_path / "patient_updated.json",
    )
    patient_composition_uuid = update_composition(ehr_id, patient_composition_id, patient_composition)
    print(f"patient_composition_uuid: {patient_composition_uuid}")

    return patient_composition_uuid


def transform_load(patient, all_disorders, all_vital_signs, ehr_id, output_path):
    """
    Transform each data instance into a composition, and POST these compositions
    to the EHRbase server

    Parameters
    ----------
    patient: Patient
        Instance of the Patient class
    all_disorders: list[Diagnosis]
        list of instances of the Diagnosis class
    all_vital_signs: list[VitalSigns]
        list of instances of the VitalSigns class
    ehr_id: UUID
        ehr_id for the given patient id
    output_path: str
        Path the the folder saving all composition outputs
    """
    print("\nPatient..")
    simplified_patient_composition = patient.model_dump_json(by_alias=True, indent=4)
    print(f"\npatient: {simplified_patient_composition}")
    patient_composition = transform_composition(
        simplified_composition=simplified_patient_composition,
        template_id="patient",
    )
    # print(f"\ncomposition: {patient_composition}")
    write_json_composition(
        composition=patient_composition,
        json_filename=output_path / "patient.json",
    )
    patient_composition_uuid = post_composition(ehr_id, patient_composition)

    print("\nSwitch patient sex at birth..")
    patient_composition_uuid = switch_patient_sex(
        patient=patient,
        ehr_id=ehr_id,
        patient_composition_id=patient_composition_uuid,
        output_path=output_path
    )

    print("\nSwitch patient sex at birth..")
    patient_composition_uuid = switch_patient_sex(
        patient=patient,
        ehr_id=ehr_id,
        patient_composition_id=patient_composition_uuid,
        output_path=output_path
    )

    # Getting versioned object uuid for deletion and retrieving all versions
    base_composition_uuid, _, _ = patient_composition_uuid.split("::")
    print(f"\nBase composition UUID: {base_composition_uuid}")

    print("\nDelete patient composition..")
    delete_composition(
        ehr_id=ehr_id,
        base_composition_uuid=base_composition_uuid
    )
    # Composition is now "deactivated", it shouldn't be updated or retrieved

    print("\nAll versions of this composition:")
    versioned_composition_uuids = get_all_versioned_composition_uuids(
        ehr_id=ehr_id,
        base_composition_uuid=base_composition_uuid
    )
    print(*versioned_composition_uuids, sep='\n')

    print("\nShow the first version of this composition:")
    print(get_composition_at_version(
        ehr_id=ehr_id,
        versioned_composition_id=versioned_composition_uuids[0]
    ))

    print("\nDiagnosis..")
    for diagnosis_i, diagnosis in enumerate(all_disorders):
        simplified_diagnosis_composition = diagnosis.model_dump_json(by_alias=True, indent=4)
        print(f"\ndiagnosis {diagnosis_i+1}: {simplified_diagnosis_composition}")
        diagnosis_composition = transform_composition(
            simplified_composition=simplified_diagnosis_composition,
            template_id="diagnosis-demo",
        )
        write_json_composition(
            composition=diagnosis_composition,
            json_filename=output_path / f"diagnosis_{diagnosis_i+1}.json",
        )
        # print(f"\ncomposition: {diagnosis_composition}")
        diagnosis_composition_uuid = post_composition(ehr_id, diagnosis_composition)
        print(f"diagnosis_composition_uuid: {diagnosis_composition_uuid}")

    print("\nVital Signs..")
    for vitalsigns_i, vitalsigns in enumerate(all_vital_signs):
        simplified_vitalsigns_composition = vitalsigns.model_dump_json(by_alias=True, indent=4)
        print(f"\nvital_signs {vitalsigns_i+1}: {simplified_vitalsigns_composition}")
        vitalsigns_composition = transform_composition(
            simplified_composition=simplified_vitalsigns_composition,
            template_id="vital_signs",
        )
        write_json_composition(
            composition=vitalsigns_composition,
            json_filename=output_path / f"vital_signs_{vitalsigns_i+1}.json",
        )
        # print(f"\ncomposition: {vitalsigns_composition}")
        vitalsigns_composition_uuid = post_composition(ehr_id, vitalsigns_composition)
        print(f"vitalsigns_composition_uuid: {vitalsigns_composition_uuid}")

    print("\nAll compositions posted for this patient [template_id, composition_uuid, time]:")
    all_compostions = retireve_all_compositions_from_ehr(ehr_id)
    print(*all_compostions, sep="\n")
