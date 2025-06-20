from pathlib import Path

#Constants
SAVE_IN_SINGLE_FILE = False
SCHEME_NAME_HA = "academic_history"
DEFAULT_COUNTRY_ID = 39 # Colombia

#File names
EXCEL_NAME = "Propuesta-datos.xlsx"

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXCEL_PATH = DATA_DIR / EXCEL_NAME
OUTPUT_DIR = DATA_DIR / "sql"

# UUID fijo del creador del usuario
CREATED_BY_UUID = "e11a3bf5-3ea4-44bd-8aae-0b67beb67b1d"
# Nombre del rol que se asignará
STUDENT_ROLE_NAME = "Estudiante"