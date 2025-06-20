import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd
from typing import Optional

class StudyLevel:
    def __init__(self, code: str, name: str, id_study_level: Optional[uuid.UUID] = None):
        if not code or not name:
            raise ValueError("StudyLevel must have a code and a name")
        self.code = code.strip()
        self.name = name.strip()
        self.id_study_level = id_study_level if id_study_level else uuid.uuid4()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.study_level (id_study_level, code, name)
VALUES ('{self.id_study_level}' :: UUID, '{self.code}', '{self.name}')
ON CONFLICT (code) DO NOTHING;"""

def generate_sql_file():
    df_study_levels = pd.read_csv("./StudyLevel/study_levels.csv", encoding="utf-8")
    # Use only unique COD_NIVEL rows
    df_study_levels = df_study_levels.drop_duplicates(subset=['COD_NIVEL'])
    
    study_levels = [
        StudyLevel(
            code=str(row['COD_NIVEL']),
            name=str(row['NIVEL'])
        )
        for _, row in df_study_levels.iterrows()
    ]
    
    with open("./StudyLevel/study_levels.sql", "w", encoding="utf-8") as f:
        for study_level in study_levels:
            f.write(study_level.to_sql())


if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")