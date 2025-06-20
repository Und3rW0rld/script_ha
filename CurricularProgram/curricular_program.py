import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd


from typing import Optional

class CurricularProgram:
    def __init__(self, code: str, name: str, snies: Optional[str], area_code: str, id_curricular_program: Optional[uuid.UUID] = None):
        if not code or not name or not area_code:
            raise ValueError("CurricularProgram must have code, name, and area_code")
        self.code = code.strip()
        self.name = name.strip()
        self.snies = snies.strip() if snies else None
        self.area_code = area_code.strip()
        self.id_curricular_program = id_curricular_program if id_curricular_program else uuid.uuid4()

    def to_sql(self) -> str:
        snies_part = f"'{self.snies}'" if self.snies else "NULL"
        return f"""INSERT INTO {SCHEME_NAME_HA}.curricular_program (id_curricular_program, code, name, snies, id_curricular_area)
VALUES ('{self.id_curricular_program}' :: UUID, '{self.code}', '{self.name}', {snies_part},
        (SELECT id_curricular_area FROM {SCHEME_NAME_HA}.curricular_area WHERE code = '{self.area_code}'))
ON CONFLICT (code) DO NOTHING;"""


def generate_sql_file():
    df_curricular_program = pd.read_csv("./CurricularProgram/curricular_programs.csv", encoding="utf-8")

    curricular_programs = [
        CurricularProgram(
            code=str(row['COD_PROG_CURRICULAR']),
            name=str(row['PROG_CURRICULAR']),
            snies=str(int(row['SNIES'])) if pd.notna(row['SNIES']) else None,
            area_code=str('99999')
        )
        for _, row in df_curricular_program.iterrows()
    ]

    with open("./CurricularProgram/curricular_program.sql", "w", encoding="utf-8") as f:
        for curricular_program in curricular_programs:
            f.write(curricular_program.to_sql())


if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")