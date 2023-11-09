# Data exploration to refine templates

import pandas as pd
import re

cd ../data


## 1. Patient demographics/informations

patients = pd.read_csv("patients.csv")

### Lookup table

print(f'There are {len(patients):,} patients')
patients.head()

### Check the date format of birth/death dates (here, YYYY-MM-DD)

patients.BIRTHDATE

### Check dead patients

dead_patients = patients[patients.DEATHDATE.notna()]
print(f'There are {len(dead_patients)} dead patients in this dataset.')
dead_patients

### Check the code value for gender (here, M or F)

patients.GENDER.unique()

## 2. Measurements of vital signs

observations = pd.read_csv("observations.csv")

### Lookup table

observations.head()

### Define the used measurement variables (a variable corresponds to approx. an archetype)

vital_signs_variables = [
    'Systolic Blood Pressure',
    'Diastolic Blood Pressure',
    'Body Height',
    'Body Weight',
    'Heart rate'
]

### For each variable, check and min-max values and the units

for variable in vital_signs_variables:
    var_df = observations[observations['DESCRIPTION']==variable]
    var_df.astype({"VALUE": float})
    print(f"{variable}: min = {var_df['VALUE'].min()} {var_df['UNITS'].iloc[0]}, max = {var_df['VALUE'].max()} {var_df['UNITS'].iloc[0]}")


## 3. Conditions (mixed of situation, finding and disorder)

conditions = pd.read_csv("conditions.csv")

### Lookup table

print(f'There are {len(conditions):,} diagnosed conditions')
conditions.head()

### Check the date format of the start/stop the diagnosed conditions (here, YYYY-MM-DD)

conditions.START


### Check conditions where the patient did not recover

conditions[conditions.STOP.isna()]

### List of all disorders

where_disorder = conditions.DESCRIPTION.apply(lambda x: bool(re.search('.*\(disorder\)', x)))
conditions[where_disorder][['CODE', 'DESCRIPTION']].drop_duplicates().sort_values('DESCRIPTION')

### List of all findings

where_finding = conditions.DESCRIPTION.apply(lambda x: bool(re.search('.*\(finding\)', x)))
conditions[where_finding][['CODE', 'DESCRIPTION']].drop_duplicates().sort_values('DESCRIPTION')

### List of all situation

where_situation = conditions.DESCRIPTION.apply(lambda x: bool(re.search('.*\(situation\)', x)))
conditions[where_situation][['CODE', 'DESCRIPTION']].drop_duplicates().sort_values('DESCRIPTION')
