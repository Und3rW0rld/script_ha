import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

def clean_text(value, max_length=None):
    if not value or pd.isna(value) or value in ["", "NULL", "None"]:
        return None
    value = str(value).strip()
    value = value.replace("'", "''")
    return value[:max_length] if max_length else value

class Subject:
    from typing import Optional
    def __init__(self, code: str, name: str, credits: int, uab_code: str, id_subject: Optional[uuid.UUID] = None):
        if not code or not name or not uab_code:
            raise ValueError("Subject must have code, name, and uab_code")

        self.id_subject = id_subject or uuid.uuid4()
        self.code = clean_text(code)
        self.name = clean_text(name)
        self.credits = credits if credits is not None else 0
        self.uab_code = uab_code.strip()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.subject (
        id_subject, code, name, credits, id_uab
        ) VALUES (
        '{self.id_subject}', '{self.code}', '{self.name}', {self.credits},
        (SELECT id_uab FROM {SCHEME_NAME_HA}.uab WHERE code = '{self.uab_code}')
        ) ON CONFLICT DO NOTHING;"""
    
def generate_sql_file():
    df_subject = pd.read_csv("./Subject/subjects.csv", encoding="utf-8")

    subjects = [
        Subject(
            code=str(row['COD_ASIG']),
            name=str(row['NOMBRE_ASIGNATURA']),
            credits=int(row['CREDITOS']) if pd.notna(row['CREDITOS']) else 0,
            uab_code="99999" #No existe el campo COD_UAB en el CSV, se usa un valor por defecto
        )
        for _, row in df_subject.iterrows()
    ]

    df_subject_2 = pd.read_csv("./Subject/subjects2.csv", encoding="utf-8")
    subjects += [
        Subject(
            code=str(row['COD_ASIG']),
            name=str(row['NOMBRE_ASIGNATURA']),
            credits=int(row['CREDITOS']) if pd.notna(row['CREDITOS']) else 0,
            uab_code= "99999",
        )
        for _, row in df_subject_2.iterrows()
    ]

    with open("./Subject/subject.sql", "w", encoding="utf-8") as f:
        for subject in subjects:
            f.write(subject.to_sql() + "\n")

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")
