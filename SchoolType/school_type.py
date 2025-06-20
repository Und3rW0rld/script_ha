import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd


class SchoolType:
    from typing import Optional
    def __init__(self, name: str, academic_mode: Optional[str] = None, id_school_type: Optional[uuid.UUID] = None):
        if not name:
            raise ValueError("SchoolType must have a name")
        self.name = name.strip()
        self.academic_mode = academic_mode.strip() if academic_mode else None
        self.id_school_type = id_school_type if id_school_type else uuid.uuid4()

    def to_sql(self) -> str:
        academic_mode_value = f"'{self.academic_mode}'" if self.academic_mode else "NULL"
        return f"""INSERT INTO {SCHEME_NAME_HA}.school_type (id_school_type, name, academic_mode)
VALUES ('{self.id_school_type}' :: UUID, '{self.name}', {academic_mode_value}) ON CONFLICT DO NOTHING ;"""


def generate_sql_file():
    df_school_types = pd.read_csv("./SchoolType/school_types.csv", encoding="utf-8")
    #remove duplicates 
    df_school_types = df_school_types.drop_duplicates(subset=['TIPO_COLEGIO', 'MODACADEMICA'])
    school_types = [
        SchoolType(
            name=str(row['TIPO_COLEGIO']),
            academic_mode=str(row['MODACADEMICA']) if pd.notna(row['MODACADEMICA']) else None
        )
        for _, row in df_school_types.iterrows()
    ]
    with open("./SchoolType/school_types.sql", "w", encoding="utf-8") as f:
        for school_type in school_types:
            f.write(school_type.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")
