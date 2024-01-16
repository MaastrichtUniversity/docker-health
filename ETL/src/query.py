"""
Functions specific to AQL queries
"""

import json
from uuid import UUID
import requests

from src.ehr import EHRBASE_BASE_URL, EHRBASE_USERRNAME, EHRBASE_PASSWORD


def retrieve_all_compositions_from_ehr(ehr_id: UUID) -> list:
    """
    Retrieve all compositions stored for a unique ehr_id and return
    a list of all composition containing the template_id, start_time and versioned_composition_id
    (showing the latest version)

    Parameters
    ----------
    ehr_id: UUID
        ehr_id for the given patient

    Returns
    -------
    list
        List of retrieved compositions for this patient. List ordered by start_time values
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
        "GET", url, headers=headers, params={"q": query}, auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD), timeout=10
    )

    response_json = json.loads(response.text)

    if response.ok:
        return response_json["rows"]
    print("No posted compositions for this patient")
    return None
