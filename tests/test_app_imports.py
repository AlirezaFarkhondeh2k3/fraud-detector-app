import os
import sys


# Add project root (parent of tests/) to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def test_app_imports():
    # Simple sanity check that the app imports without crashing
    import app  # noqa: F401
