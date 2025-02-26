import logging
import os

import requests
from flask import Flask, request, Response

app = Flask(__name__)

logging.basicConfig(
    level="INFO",
    format="%(asctime)s ~ %(levelname)s:%(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

base_server_url = "https://terminologieserver.nl"


def connect():
    url = base_server_url + "/auth/realms/nictiz/.well-known/openid-configuration"
    logging.info(f"Retrieving {url}")
    req = requests.get(url).json()
    token_endpoint = req.get("token_endpoint")
    end_session_endpoint = req.get("end_session_endpoint")

    username = os.environ.get("TERMINOLOGY_USERNAME")
    password = os.environ.get("TERMINOLOGY_PASSWORD")

    if not username or not password:
        exit("Set the credential correctly")

    # Login request uitvoeren
    data = {
        "grant_type": "password",
        "client_id": "cli_client",
        "username": username,
        "password": password,
    }
    req = requests.post(token_endpoint, data=data)
    response = req.json()
    access_token = response.get("access_token")

    logging.info("-" * 60)
    logging.info("*** Inloggen ***")
    logging.info(f"Status code: {req.status_code}")
    if req.status_code != 200:
        logging.critical("Response not 200")
        logging.critical(response)
        exit()
    logging.info("-" * 60)
    logging.info("")

    return access_token, end_session_endpoint


@app.route("/<path:path>", methods=["GET"])
def proxy(path):
    token, end_session_endpoint = connect()

    server_url = f"{base_server_url}/fhir"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/fhir+json",
    }
    req_url = server_url + request.full_path
    resp = requests.get(req_url, headers=headers)

    if resp.status_code == 401:
        token, end_session_endpoint = connect()
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/fhir+json",
        }
        resp = requests.get(req_url, headers=headers)

    excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)

    logout(token, end_session_endpoint)

    return response


def logout(token, end_session_endpoint):
    # Uitloggen
    logging.info("-" * 60)
    logging.info(f"*** Uitloggen ***")
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/fhir+json",
    }

    response = requests.get(end_session_endpoint, headers=headers)
    logging.info(f"Status code: {response.status_code}")
    if response.status_code != 200:
        logging.critical("Response not 200")
        logging.critical(response)
        exit()
    logging.info("-" * 60)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
