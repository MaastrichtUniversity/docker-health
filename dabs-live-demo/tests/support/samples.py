"""Load the test-only federation payloads from ``tests/samples/``.

The samples are materialised from ``docs/federation-samples.md`` (see
``tests/samples/README.md`` for what is verbatim vs generated). They are *not* a
product fixture set: only the tests import this module.
"""

import json
import pathlib

SAMPLES_DIR = pathlib.Path(__file__).resolve().parents[1] / "samples"

ENDPOINTS = ["Patient", "Bloeddruk", "Lichaamsgewicht", "LichaamsLengte"]

# Documented per-endpoint totals for BSN 999990603.
EXPECTED_COUNTS = {
    "Patient": 4,
    "Bloeddruk": 24,
    "Lichaamsgewicht": 24,
    "LichaamsLengte": 4,
}

# Documented per-node counts.
EXPECTED_PER_NODE = {
    "Patient": 1,
    "Bloeddruk": 6,
    "Lichaamsgewicht": 6,
    "LichaamsLengte": 1,
}

KNOWN_NODES = ["zio", "envida", "mumc", "vitala"]


def load(endpoint: str) -> list:
    """Return one endpoint's flat live list."""
    return json.loads((SAMPLES_DIR / f"{endpoint}.json").read_text(encoding="utf-8"))


def load_all() -> dict:
    return {endpoint: load(endpoint) for endpoint in ENDPOINTS}
