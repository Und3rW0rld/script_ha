import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd
from typing import Optional

class UniversitySite:
    def __init__(self, code: str, name: str, id_university_site: Optional[uuid.UUID] = None):
        if not code or not name:
            raise ValueError("UniversitySite must have code and name")
        self.code = code.strip()
        self.name = name.strip()
        self.id_university_site = id_university_site if id_university_site else uuid.uuid4()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.university_site (id_university_site, code, name)
VALUES ('{self.id_university_site}' :: UUID, '{self.code}', '{self.name}')
ON CONFLICT (code) DO NOTHING;"""

def generate_sql_file():
    df_university_sites = pd.read_csv("./UniversitySite/university_sites.csv", encoding="utf-8")

    university_sites = [
        UniversitySite(
            code=str(row['COD_SEDE']),
            name=str(row['SEDE'])
        )
        for _, row in df_university_sites.iterrows()
    ]

    with open("./UniversitySite/university_sites.sql", "w", encoding="utf-8") as f:
        for university_site in university_sites:
            f.write(university_site.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")