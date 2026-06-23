import sys
import os

# Ensure the root project directory is in the Python path
# This allows 'from app import app' to work seamlessly
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import app
