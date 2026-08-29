"""Lets the tests import our program files from the folder above."""

import sys
from pathlib import Path

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_FOLDER))
