import jwt
from jwt import PyJWKClient
import json
import time
import requests
import uuid

# URL of the JWK Set provided by the authorization server
# JWK_SET_URL = "http://127.0.0.1:8080/.well-known/jwks.json"
JWK_SET_URL = "https://datahubmaastricht.nl/files/jwks-non-prod-mumc.json"
# JWK_SET_URL = "https://fhir.epic.com/interconnect-fhir-oauth/.well-known/jwks.json"

def verify_jwt(token: str, jwk_url: str = JWK_SET_URL) -> dict:
    """Verify a JWT using a remote JWK Set.

    Returns the decoded payload if verification succeeds, otherwise raises an
    exception from ``jwt``.
    """
    # The token may lack a 'kid' header. If so, fall back to the first key in the JWKS.
    signing_key = PyJWKClient(jwk_url).get_signing_key_from_jwt(token)
    # try:
    #     signing_key = PyJWKClient(jwk_url).get_signing_key_from_jwt(token)
    # except Exception:
    #     signing_key = PyJWKClient(jwk_url).get_signing_keys()[0]
    # # Determine algorithm from token header (fallback to RS256)
    # try:
    header = jwt.get_unverified_header(token)
    alg = header.get("alg", "RS256")
    # except Exception:
    #     alg = "RS256"
    return jwt.decode(token, signing_key.key, algorithms=[alg], audience="https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token")


def get_jwt_token():
    """Obtain an access token using client credentials.

    The function creates a JWT signed with the local private key and exchanges it
    for an access token at Epic's token endpoint.
    """
    # read and load the key
    private_key_pem = open('privatekey.pem', 'r').read()

    public_key_pem = open('publickey509.pem', 'r').read()

    epoch_time = int(time.time()) + 240

    print(epoch_time)

    payload = {
        "iss": "62760e86-74be-4099-822d-1af7762c5d4d",
        "sub": "62760e86-74be-4099-822d-1af7762c5d4d",
        "aud": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
        #"jti": "f9eaafba-2e49-11ea-8880-5ce0c5aee679", ## new uuid for each run
        "jti": str(uuid.uuid4()),
        "exp": epoch_time
    }

    headers = {
        "typ": "JWT",
        "kid": "qM4y9Eqej9Z1pgdAhU47xKpd9RVwhk6C7CgSUYh4res",
        "jku": JWK_SET_URL
    }

    encoded_jwt = jwt.encode(payload, private_key_pem, algorithm="RS384", headers=headers)

    print("Client assertion JWT:", encoded_jwt)
    header = jwt.get_unverified_header(encoded_jwt)
    print("Header:", header)
    verified = verify_jwt(encoded_jwt)
    print("verify_jwt:", verified)

    # decode = jwt.decode(encoded_jwt, key = public_key_pem , algorithms=["RS384"])

    data = {
        "grant_type": "client_credentials",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": encoded_jwt
    }

    response = requests.post("https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token", data=data)
    access = response.json()
    print(access)

    # # Optional: verify the access token if you have Epic's JWKS.
    # decoded_payload = verify_jwt(access["access_token"])
    # print("Decoded access token payload:", json.dumps(decoded_payload, indent=2))
    return access["access_token"]


if __name__ == "__main__":
    print(get_jwt_token())
    # print(verify_jwt(get_jwt_token()))
