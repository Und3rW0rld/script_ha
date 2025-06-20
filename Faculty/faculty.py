import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd
from typing import Optional

class Faculty:
    def __init__(self, code: str, name: str, university_site_code: str, id_faculty: Optional[uuid.UUID] = None):
        if not code or not name or not university_site_code:
            raise ValueError("Faculty must have code, name, and university_site_code")
        self.code = code.strip()
        self.name = name.strip()
        self.university_site_code = university_site_code.strip()
        self.id_faculty = id_faculty if id_faculty else uuid.uuid4()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.faculty (id_faculty, code, name, id_university_site)
VALUES (
    '{self.id_faculty}' :: UUID,
    '{self.code}',
    '{self.name}',
    (SELECT id_university_site FROM {SCHEME_NAME_HA}.university_site WHERE code = '{self.university_site_code}')
)
ON CONFLICT (code) DO NOTHING;"""


def generate_sql_file():
    df_faculty = pd.read_csv("./Faculty/faculty.csv", encoding="utf-8")

    faculties = [
        Faculty(
            code=str(row['COD_FACULTAD']),
            name=str(row['FACULTAD']),
            university_site_code=str(row['COD_SEDE'])
        )
        for _, row in df_faculty.iterrows()
    ]

    with open("./Faculty/faculty.sql", "w", encoding="utf-8") as f:
        for faculty in faculties:
            f.write(faculty.to_sql())   

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")