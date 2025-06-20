import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class AdmissionSubaccess:
    from typing import Optional
    def __init__(self, code: str, name: str, id_admission_subaccess: Optional[uuid.UUID] = None):
        if not code or not name:
            raise ValueError("AdmissionSubaccess must have a code and a name")
        self.code = code.strip()
        self.name = name.strip()
        self.id_admission_subaccess = id_admission_subaccess if id_admission_subaccess else uuid.uuid4()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.admission_subaccess (id_admission_subaccess, code, name)
VALUES ('{self.id_admission_subaccess}' :: UUID, '{self.code}', '{self.name}')
ON CONFLICT (code) DO NOTHING;"""


def generate_sql_file():
    df_admission_subaccess = pd.read_csv("./AdmissionSubaccess/admission_subaccess.csv", encoding="utf-8")
    codes = set()
    codes = {str(code) for code in codes if pd.notna(code)}
    # Remove duplicates
    df_admission_subaccess = df_admission_subaccess.drop_duplicates(subset=['COD_SUBACCESO', 'SUBACCESO'])
    
    admission_subaccesses = [
        AdmissionSubaccess(
            code=str(row['COD_SUBACCESO']),
            name=str(row['SUBACCESO'])
        )
        for _, row in df_admission_subaccess.iterrows()
    ]
    
    for admission_subaccess in admission_subaccesses:
        if admission_subaccess.code in codes:
            new_code = admission_subaccess.code
            while new_code in codes:
                new_code += "A"
            admission_subaccess.code = new_code
            codes.add(new_code)
        else:
            codes.add(admission_subaccess.code)

    with open("./AdmissionSubaccess/admission_subaccess.sql", "w", encoding="utf-8") as f:
        for admission_subaccess in admission_subaccesses:
            f.write(admission_subaccess.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")