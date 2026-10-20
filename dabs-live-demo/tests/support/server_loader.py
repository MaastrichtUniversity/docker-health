"""Load ``dabs-live-demo/server.py`` as a module for unit tests.

The application is a script, not an installed package, so we load it by path. A single
cached module instance is shared by every test in a run; each test restores any
``CONFIG`` or module attribute it changes in ``setUp``/``tearDown``.
"""

import importlib.util
import pathlib
import sys

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
SERVER_PATH = PROJECT_ROOT / "server.py"

_MODULE_NAME = "dabs_server_under_test"


def load_server():
    if _MODULE_NAME in sys.modules:
        return sys.modules[_MODULE_NAME]
    spec = importlib.util.spec_from_file_location(_MODULE_NAME, SERVER_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[_MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module
