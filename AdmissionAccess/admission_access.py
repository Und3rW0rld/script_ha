import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class AdmissionAccess:
    from typing import Optional
    def __init__(self, code: str, name: str, id_admission_access: Optional[uuid.UUID] = None):
        if not code or not name:
            raise ValueError("AdmissionAccess must have code and name")
        
        self.id_admission_access = id_admission_access or uuid.uuid4()
        self.code = code.strip()
        self.name = name.strip()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.admission_access (
            id_admission_access, code, name
        ) VALUES (
            '{self.id_admission_access}', '{self.code}', '{self.name}'
        )
        ON CONFLICT (code) DO NOTHING;"""

def generate_sql_file():
    df_admission_access = pd.read_csv("./AdmissionAccess/admission_access.csv", encoding="utf-8")
    admission_accesses = [
        AdmissionAccess(
            code=str(row['COD_ACCESO']),
            name=str(row['ACCESO'])
        )
        for _, row in df_admission_access.iterrows()
    ]
    with open("./AdmissionAccess/admission_access.sql", "w", encoding="utf-8") as f:
        for admission_access in admission_accesses:
            f.write(admission_access.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")