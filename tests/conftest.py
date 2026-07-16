import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DAGS_DIR = ROOT_DIR / "dags"

os.environ.setdefault("AIRFLOW_HOME", str(ROOT_DIR / ".airflow_test_home"))

sys.path.insert(0, str(DAGS_DIR))
