import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd
from typing import Optional

class CurricularArea:
    def __init__(self, code: str, name: str, id_curricular_area: Optional[uuid.UUID] = None):
        if not code or not name:
            raise ValueError("CurricularArea must have code and name")
        self.code = code.strip()
        self.name = name.strip()
        self.id_curricular_area = id_curricular_area if id_curricular_area else uuid.uuid4()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.curricular_area (id_curricular_area, code, name)
VALUES ('{self.id_curricular_area}' :: UUID, '{self.code}', '{self.name}')
ON CONFLICT (code) DO NOTHING;"""

def generate_sql_file():
    df_curricular_area = pd.read_csv("./CurricularArea/curricular_areas.csv", encoding="utf-8")

    curricular_areas = [
        CurricularArea(
            code=str(row['COD_AREA_CURRICULAR']),
            name=str(row['AREA_CURRICULAR'])
        )
        for _, row in df_curricular_area.iterrows()
    ]

    with open("./CurricularArea/curricular_area.sql", "w", encoding="utf-8") as f:
        for curricular_area in curricular_areas:
            f.write(curricular_area.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")