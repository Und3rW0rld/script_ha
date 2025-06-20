import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

from typing import Optional

class StudyPlan:
    def __init__(self, code: str, name: str, credits: Optional[int], agreement: Optional[str],
                 study_level_code: str, curricular_program_code: str, faculty_code: str):
        if not code or not name:
            raise ValueError("StudyPlan must have code and name")

        self.code = code.strip()
        self.name = name.strip()
        self.credits = credits
        self.agreement = agreement.strip() if agreement else None
        self.study_level_code = study_level_code
        self.curricular_program_code = curricular_program_code
        self.faculty_code = faculty_code
        self.id = uuid.uuid4()

    def to_sql(self) -> str:
        return f"""
        INSERT INTO {SCHEME_NAME_HA}.study_plan (
            id_study_plan, code, name, credits, agreement,
            id_study_level, id_curricular_program, id_faculty
        ) VALUES (
            '{self.id}', '{self.code}', '{self.name}', {self.credits or 'NULL'},
            {'NULL' if not self.agreement else f"'{self.agreement}'"},
            (SELECT id_study_level FROM {SCHEME_NAME_HA}.study_level WHERE name = '{self.study_level_code}'),
            (SELECT id_curricular_program FROM {SCHEME_NAME_HA}.curricular_program WHERE code = '{self.curricular_program_code}'),
            (SELECT id_faculty FROM {SCHEME_NAME_HA}.faculty WHERE code = '{self.faculty_code}')
        ) ON CONFLICT DO NOTHING;
        """


def generate_sql_file():
    df_study_plan = pd.read_csv("./StudyPlan/study_plans.csv", encoding="utf-8")

    study_plans = [
        StudyPlan(
            code=str(row['COD_PLAN']),
            name=str(row['PLAN_ESTUDIOS']),
            credits=int(row['CREDITOS_REQUERIDOS_PLAN']) if pd.notna(row['CREDITOS_REQUERIDOS_PLAN']) else None,
            agreement= None ,
            study_level_code=str(row['TIPO_NIVEL']),
            curricular_program_code=str(row['COD_PROG_CURRICULAR']),
            faculty_code=str(row['COD_FACULTAD'])
        )
        for _, row in df_study_plan.iterrows()
    ]

    with open("./StudyPlan/study_plan.sql", "w", encoding="utf-8") as f:
        for study_plan in study_plans:
            f.write(study_plan.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")