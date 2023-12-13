"""
Functions to POST and GET templates from the EHRbase
"""

import os
import json
import xml.etree.ElementTree as ET
import requests

EHRBASE_USERRNAME = os.environ['EHRBASE_USERRNAME']
EHRBASE_PASSWORD = os.environ['EHRBASE_PASSWORD']
EHRBASE_BASE_URL = os.environ['EHRBASE_BASE_URL']


def fetch_all_templates() -> None:
    """
    Print all template available on the server
    """
    url = f"{EHRBASE_BASE_URL}/definition/template/adl1.4"

    headers = {
        'Accept': 'application/json',
        'Prefer': 'return=minimal',
    }

    response = requests.request(
        'GET',
        url,
        headers=headers,
        auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
        timeout=10
    )
    if response.ok:
        response_json = json.loads(response.text)
        for template in response_json:
            print(f"concept: {template['concept']}")
            print(f"template_id: {template['template_id']}")
            print(f"archetype_id: {template['archetype_id']}")
            print(f"create_timestamp: {template['created_timestamp']}")


def post_template(filename: str) -> None:
    """
    Post a template to the server. The template is provided as a filename which will be loaded
    Parameters
    ----------
    filename: str
        Name of the template that be loaded  from disk
    """
    url = f'{EHRBASE_BASE_URL}/definition/template/adl1.4'

    headers = {
        'Accept': 'application/xml',
        'Prefer': 'return=minimal',
        'Content-Type': 'application/xml'
    }

    print(filename)
    with open(filename, 'rb') as payload:
        response = requests.request(
            'POST',
            url,
            headers=headers,
            data=payload.read(),
            auth=(EHRBASE_USERRNAME, EHRBASE_PASSWORD),
            timeout=10
        )

    print(f'RESPONSE: {response.status_code}')
    if response.ok:
        print(f'Template {filename} was successfully created')
    else:
        # Convert XML output text to Dictionary:
        response_text = {'error': None, 'message': None}
        for item in ET.fromstring(response.content):
            response_text[item.tag] = item.text
        print(f'ERROR {response_text['error']}')
        print(response_text['message'])
