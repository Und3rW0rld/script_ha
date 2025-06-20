import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class Period:
    from typing import Optional
    def __init__(self, name: str, code: Optional[str] = None, id_period: Optional[uuid.UUID] = None):

        if not name:
            raise ValueError("Period must have a name")
        self.code = (code or name[:3].upper()).strip()
        self.name = name.strip()
        self.id_period = id_period if id_period else uuid.uuid4()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.period (id_period, code, name)
            VALUES (
                '{self.id_period}' :: UUID, '{self.code}', '{self.name}'
            )
            ON CONFLICT (code) DO NOTHING;"""

def generate_sql_file():
    df_period = pd.read_csv("./Period/subjects.csv", encoding="utf-8")

    #remove duplicates based on 'PERIODO_ASIG_NUM'
    df_period = df_period.drop_duplicates(subset='PERIODO_ASIG_NUM')

    codes = set()
    periods = []
    for _, row in df_period.iterrows():
        codes.add(str(row['PERIODO_ASIG_NUM']))
        periods.append(
            Period(
                name=str(row['PERIODO_ASIG_NUM']),
                code=str(row['PERIODO_ASIG_NUM']) if pd.notna(row['PERIODO_ASIG_NUM']) else None
            )
            
        )

    df_period_2 = pd.read_csv("./Period/subjects2.csv", encoding="utf-8")
    df_period_2 = df_period_2.drop_duplicates(subset='PERIODO_ASIG_NUM')

    periods += [
        Period(
            name=str(row['PERIODO_ASIG_NUM']),
            code=str(row['PERIODO_ASIG_NUM']) if pd.notna(row['PERIODO_ASIG_NUM']) else None
        )
        for _, row in df_period_2.iterrows() if str(row['PERIODO_ASIG_NUM']) not in codes
    ]

    with open("./Period/period.sql", "w", encoding="utf-8") as f:
        for period in periods:
            f.write(period.to_sql() + "\n")

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")