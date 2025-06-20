import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class Municipality:
    from typing import Optional
    def __init__(self, code: str, name: str, state_code: str, id_municipality: Optional[uuid.UUID] = None):
        if not code or not name or not state_code:
            raise ValueError("Municipality must have code, name, and state_code")
        
        self.id_municipality = id_municipality or uuid.uuid4()
        self.code = code.strip()
        self.name = name.strip()
        self.state_code = state_code.strip()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.municipality (
            id_municipality, code, name, id_state
        ) VALUES (
            '{self.id_municipality}', '{self.code}', '{self.name}',
            (SELECT id_state FROM {SCHEME_NAME_HA}.state WHERE code = '{self.state_code}')
        ) ON CONFLICT DO NOTHING ;"""

def generate_sql_file():
    df_municipalities = pd.read_csv("./Municipality/municipalities.csv", encoding="utf-8")
    municipalities = [
        Municipality(
            code=str(row['COD_MUNICIPIO']),
            name=str(row['MUNICIPIO']),
            state_code=str(row['COD_DEPARTAMENTO'])
        )
        for _, row in df_municipalities.iterrows()
    ]

    with open("./Municipality/municipalities.sql", "w", encoding="utf-8") as f:
        for municipality in municipalities:
            f.write(municipality.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")