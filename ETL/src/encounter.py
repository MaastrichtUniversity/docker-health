

class Encounter:
    """Data model for encounter"""
    def __init__(self, identifier, startdate, stopdate, patient_id):
        self.id = identifier # int
        self.startdate = startdate # datetime
        self.stopdate = stopdate     # datetime
        self.patient_id = patient_id # patient_id


def parse_all_encounters(encounters_df):
    all_encounters = {}
    for _, encounter in encounters_df.iterrows():
        encounter_id = encounter["Id"]
        startdate = encounter["START"]
        stopdate = encounter["STOP"]
        patient_id = encounter["PATIENT"]
        all_encounters[encounter_id] = Encounter(encounter_id, startdate, stopdate, patient_id)
    return all_encounters