import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class AcademicFile:
    from typing import Optional
    def __init__(
        self,
        code: str,
        id_student: str,
        id_study_plan: str,
        id_student_admission: str,
        id_academic_file: Optional[uuid.UUID] = None
    ):
        self.id_academic_file = id_academic_file or uuid.uuid4()
        self.code = code
        self.id_student = id_student
        self.id_study_plan = id_study_plan
        self.id_student_admission = id_student_admission

    def to_sql(self):
        return f"""INSERT INTO {SCHEME_NAME_HA}.academic_file (
            id_academic_file, code, id_student, id_study_plan, id_student_admission
        ) VALUES (
            '{self.id_academic_file}', '{self.code}', {self.id_student},
            {self.id_study_plan}, {self.id_student_admission}
        ) ON CONFLICT DO NOTHING;"""

def generate_sql_file():
    df_academic_file = pd.read_csv("./AcademicFile/academic_files.csv", encoding="utf-8")
    academic_files = []
    for _, row in df_academic_file.iterrows():
        id_student = f"(SELECT id_student FROM {SCHEME_NAME_HA}.student WHERE code = '{row['CODIGO_INTERNO']}' LIMIT 1)"
        id_study_plan = f"(SELECT id_study_plan FROM {SCHEME_NAME_HA}.study_plan WHERE code = '{row['COD_PLAN_ESTUDIOS']}' LIMIT 1)"
        id_student_admission = (
            f"(SELECT id_student_admission FROM {SCHEME_NAME_HA}.student_admission "
            f"WHERE id_student = {id_student} LIMIT 1)"
        )
        academic_files.append(
            AcademicFile(
                code=str(row['HIST_ACAEMICA']),
                id_student=id_student,
                id_study_plan=id_study_plan,
                id_student_admission=id_student_admission
            )
        )
    with open("./AcademicFile/academic_file.sql", "w", encoding="utf-8") as f:
        for academic_file in academic_files:
            f.write(academic_file.to_sql() + "\n")

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")
