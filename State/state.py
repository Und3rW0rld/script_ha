import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class State:
    from typing import Optional

    def __init__(self, code: str, name: str, id_state: Optional[uuid.UUID] = None):
        if not code or not name:
            raise ValueError("State must have a code and a name")
        
        self.id_state = id_state or uuid.uuid4()
        self.code = code.strip()
        self.name = name.strip()
    
    def to_sql(self) -> str:

        return f"""INSERT INTO {SCHEME_NAME_HA}.state (
            id_state, code, name
        ) VALUES (
            '{self.id_state}', '{self.code}', '{self.name}'
        ) ON CONFLICT DO NOTHING;"""

    def __repr__(self):
        return f"<State {self.code} - {self.name}>"

def generate_sql_file():
    df_states = pd.read_csv("./State/states.csv", encoding="utf-8")
    states = [
        State(
            code=str(row['COD_DEPARTAMENTO']),
            name=str(row['DEPARTAMENTO'])
        )
        for _, row in df_states.iterrows()
    ]

    with open("./State/states.sql", "w", encoding="utf-8") as f:
        for state in states:
            f.write(state.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")