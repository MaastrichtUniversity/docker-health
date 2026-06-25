import json
import hashlib
from jwt import algorithms
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# # ----------------------------------------------------------------------
# # Load the X.509 certificate and extract the RSA public key
# # ----------------------------------------------------------------------
# with open('publickey509.pem', 'rb') as f:
#     cert_pem = f.read()
#
# certificate = x509.load_pem_x509_certificate(cert_pem, backend=default_backend())
# public_key = certificate.public_key()

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

with open('privatekey.pem', 'rb') as f:
    priv_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

public_key = priv_key.public_key()

# ----------------------------------------------------------------------
# Convert the public key to a JWK (JSON Web Key) representation
# ----------------------------------------------------------------------
# `to_jwk` returns a JSON string; parse it back to a dict
jwk_json_str = algorithms.RSAAlgorithm.to_jwk(public_key)
jwk_dict = json.loads(jwk_json_str)

# ----------------------------------------------------------------------
# Add a deterministic key ID (kid) – use a SHA‑256 thumbprint of the key
# ----------------------------------------------------------------------
# The thumbprint is the base64url‑encoded SHA‑256 hash of the JWK members
# required by RFC 7638 (kty, n, e).  PyJWT does not compute it automatically,
# so we create it manually.
thumbprint_input = (
    f"{{\"e\":\"{jwk_dict['e']}\",\"kty\":\"{jwk_dict['kty']}\",\"n\":\"{jwk_dict['n']}\"}}"
).encode('utf-8')
kid = hashlib.sha256(thumbprint_input).digest()
# base64url‑encode without padding
kid_b64 = (
    __import__('base64')
    .urlsafe_b64encode(kid)
    .decode('utf-8')
    .rstrip('=')
)
# Add the computed kid and other required fields
jwk_dict["kid"] = kid_b64
jwk_dict["use"] = "sig"
jwk_dict["alg"] = "RS384"

# ----------------------------------------------------------------------
# Build the final JWK Set
# ----------------------------------------------------------------------
jwks = {"keys": [jwk_dict]}

# ----------------------------------------------------------------------
# Write the JWK Set to a file
# ----------------------------------------------------------------------
with open('jwks.json', 'w') as f:
    json.dump(jwks, f, indent=2)

print('JWK Set written to jwks.json')
print('kid (key id) =', kid_b64)
