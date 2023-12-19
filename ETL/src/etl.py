"""
Functions to extract demo data from various input formats.
Create object instances for single patient: Patient, Diagnosis and VitalSigns.
Transform each data instance into a composition.
Load each composition to the EHRbase server.
"""

import re
import json
import pandas as pd

from src.composition import (
    transform_composition,
    post_composition,
    write_json_composition
)

from src.patient import (
    Patient,
    parse_patient_csv,
    parse_patient_json,
    create_patient_instance
)
from src.diagnosis import (
    Diagnosis,
    parse_all_diagnosis_csv,
    parse_all_diagnosis_json,
    create_diagnosis_instance
)
from src.vitalsigns import (
    VitalSigns,
    parse_vital_signs_csv,
    parse_vital_signs_json,
    create_vital_signs_instance
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
    patients_df = pd.read_csv(data_path / 'patients.csv')
    conditions_df = pd.read_csv(data_path / 'conditions.csv')
    observations_df = pd.read_csv(data_path / 'observations.csv')
    encounters_df = pd.read_csv(data_path / 'encounters.csv')
    # all_encounters = parse_all_encounters(encounters_df)

    print("\nPatient..", end='\t')
    patient_df = patients_df[patients_df['Id'] == patient_id]
    patient = create_patient_instance(*parse_patient_csv(patient_df))
    print(f"information extracted for patient_id: {patient_id}")

    print("\nDiagnosis..", end='\t')
    where_disorder = conditions_df['DESCRIPTION'].apply(
        lambda x: bool(re.search('.*(disorder)', x))
    )
    patient_disorders_df = conditions_df[where_disorder][conditions_df['PATIENT'] == patient_id]
    all_disorders = []
    for _, disorder_df in patient_disorders_df.iterrows():
        all_disorders.append(create_diagnosis_instance(*parse_all_diagnosis_csv(disorder_df)))
    print(f"{len(all_disorders)} disorders reported for this patient.")

    print("\nVital Signs..", end='\t')
    patient_encounter_ids = encounters_df[encounters_df['PATIENT'] == patient_id]['Id'].tolist()
    vital_signs_df = observations_df[
        (observations_df['ENCOUNTER'].isin(patient_encounter_ids)) & \
        (observations_df['CATEGORY'] == 'vital-signs')
        # (observations_df['DESCRIPTION'].isin(VITAL_SIGNS_UNITS.keys()))
    ]

    all_vital_signs = []
    for encounter_id in patient_encounter_ids:
        vital_signs_enc_df = vital_signs_df[vital_signs_df['ENCOUNTER'] == encounter_id]
        if vital_signs_enc_df.shape[0] == 0:
            # print(f"Encounter id {encounter_id} has no vital signs observations")
            continue

        all_vital_signs.append(create_vital_signs_instance(
            parse_vital_signs_csv(vital_signs_enc_df),
            vital_signs_units
        ))
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
    with open(data_path / f"{patient_id}.json", encoding='utf-8') as infile:
        patient_json = json.load(infile)

    print("\nPatient..", end='\t')
    patient = create_patient_instance(*parse_patient_json(patient_json))
    print(f"information extracted for patient_id: {patient_id}")

    print("\nDiagnosis..", end='\t')
    all_disorders = []
    for encounter_i, encounter in enumerate(patient_json['record']['encounters']):
        if 'conditions' in encounter:
            for condition_j, condition in enumerate(encounter['conditions']):
                description = condition['codes'][0]['display']
                if not bool(re.search('.*(disorder)', description)):
                    # print("Current condition is not classified as a disorder.")
                    continue
                all_disorders.append(create_diagnosis_instance(
                    *parse_all_diagnosis_json(patient_json, encounter_i, condition_j))
                )
    print(f"{len(all_disorders)} disorders reported for this patient.")

    print("\nVital Signs..")
    all_vital_signs = []
    for encounter_i, encounter in enumerate(patient_json['record']['encounters']):
        if encounter['observations'] == []:
            # print(f"Encounter id {encounter_i} has no vital signs observations")
            continue
        list_observations_j = []
        for observation_j, observation in enumerate(encounter['observations']):
            if observation['category'] == 'vital-signs':
                list_observations_j.append(observation_j)

        all_vital_signs.append(create_vital_signs_instance(
            parse_vital_signs_json(patient_json, encounter_i, list_observations_j),
            vital_signs_units
        ))
    print(f"{len(all_vital_signs)} vital signs reported for this patient.")

    return patient, all_disorders, all_vital_signs


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
        template_id='patient'
    )
    # print(f"\ncomposition: {patient_composition}")
    write_json_composition(
        composition=patient_composition,
        json_filename=output_path / 'patient.json'
    )
    patient_composition_uuid = post_composition(ehr_id, patient_composition)
    print(f"patient_composition_uuid: {patient_composition_uuid}")

    print("\nDiagnosis..")
    for diagnosis_i, diagnosis in enumerate(all_disorders):
        simplified_diagnosis_composition = diagnosis.model_dump_json(by_alias=True, indent=4)
        print(f"\ndiagnosis {diagnosis_i+1}: {simplified_diagnosis_composition}")
        diagnosis_composition = transform_composition(
            simplified_composition=simplified_diagnosis_composition,
            template_id="diagnosis-demo"
        )
        write_json_composition(
            composition=diagnosis_composition,
            json_filename=output_path / f'diagnosis_{diagnosis_i+1}.json'
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
            template_id='vital_signs'
        )
        write_json_composition(
            composition=vitalsigns_composition,
            json_filename=output_path / f'vital_signs_{vitalsigns_i+1}.json'
        )
        # print(f"\ncomposition: {vitalsigns_composition}")
        vitalsigns_composition_uuid = post_composition(ehr_id, vitalsigns_composition)
        print(f"vitalsigns_composition_uuid: {vitalsigns_composition_uuid}")
