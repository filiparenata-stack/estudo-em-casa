import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
DIR_API = os.path.join(DIR, "api")
if DIR_API not in sys.path:
    sys.path.insert(0, DIR_API)
if DIR not in sys.path:
    sys.path.insert(0, DIR)

from api.app import app
