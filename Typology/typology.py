import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class Typology:
    from typing import Optional
    def __init__(self, name: str, code: Optional[str] = None, id_typology: Optional[uuid.UUID] = None):

        if not name:
            raise ValueError("Typology must have a name")
        self.code = (code or name[:3].upper()).strip()
        self.name = name.strip()
        self.id_typology = id_typology if id_typology else uuid.uuid4()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.typology (id_typology, code, name)
VALUES (
    '{self.id_typology}', '{self.code}', '{self.name}'
)
ON CONFLICT (code) DO NOTHING;"""
    

def generate_sql_file():
    codes = set()
    df_typology = pd.read_csv("./Typology/subjects.csv", encoding="utf-8")

    df_typology = df_typology.drop_duplicates(subset=['TIPOLOGIA', 'TIPOLOGIA_2'])
    df_typology = df_typology.dropna(subset=['TIPOLOGIA'])

    typologies = []

    for _, row in df_typology.iterrows():
        typologies.append(
            Typology(
                name=str(row['TIPOLOGIA_2']),
                code=str(row['TIPOLOGIA']) if pd.notna(row['TIPOLOGIA']) else None,
            )
        )
        codes.add(str(row['TIPOLOGIA']))

    

    df_typology_2 = pd.read_csv("./Typology/subjects2.csv", encoding="utf-8")
    df_typology_2 = df_typology_2.drop_duplicates(subset=['TIPOLOGIA', 'TIPOLOGIA_2'])
    df_typology_2 = df_typology_2.dropna(subset=['TIPOLOGIA'])
    for _, row in df_typology_2.iterrows():
        if str(row['TIPOLOGIA']) not in codes:
            codes.add(str(row['TIPOLOGIA']))
            typologies.append(
                Typology(
                    name=str(row['TIPOLOGIA_2']),
                    code=str(row['TIPOLOGIA']) if pd.notna(row['TIPOLOGIA']) else None,
                )
            )
    

    with open("./Typology/typology.sql", "w", encoding="utf-8") as f:
        for typology in typologies:
            f.write(typology.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")