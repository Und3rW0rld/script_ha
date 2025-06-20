import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class Uab:
    from typing import Optional
    def __init__(self, code: str, name: str, faculty_code: Optional[str] = None, id_uab: Optional[uuid.UUID] = None):
        if not code or not name:
            raise ValueError("UAB must have code and name")
        
        self.code = code.strip()
        self.name = name.strip()
        self.faculty_code = faculty_code.strip() if faculty_code else None
        self.id_uab = id_uab if id_uab else uuid.uuid4()

    def to_sql(self) -> str:
        faculty_sql = (
            f"(SELECT id_faculty FROM {SCHEME_NAME_HA}.faculty WHERE code = '{self.faculty_code}')"
            if self.faculty_code else "NULL"
        )

        return f"""INSERT INTO {SCHEME_NAME_HA}.uab (id_uab, code, name, id_faculty)
VALUES (
    '{self.id_uab}' :: UUID,
    '{self.code}',
    '{self.name}',
    {faculty_sql}
)
ON CONFLICT (code) DO NOTHING;"""


def generate_sql_file():
    df_uab = pd.read_csv("./Uab/uab.csv", encoding="utf-8")

    uabs = [
        Uab(
            code=str(row['COD_UAB']),
            name=str(row['UAB']),
            faculty_code=str(row['COD_FACULTAD']) if pd.notna(row['COD_FACULTAD']) else None
        )
        for _, row in df_uab.iterrows()
    ]

    with open("./Uab/uab.sql", "w", encoding="utf-8") as f:
        for uab in uabs:
            f.write(uab.to_sql())


if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")