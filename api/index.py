import os
import sys

# Make the project root importable when this file runs as a Vercel function.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app  # noqa: E402

# Vercel's Python builder picks up the Flask app exposed as `app`.
