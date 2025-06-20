import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class AdmissionStartNode:
    from typing import Optional
    def __init__(self, code: str, name: str, id_admission_start_node: Optional[uuid.UUID] = None):
        if not code or not name:
            raise ValueError("AdmissionStartNode must have a code and a name")
        self.code = code.strip()
        self.name = name.strip()
        self.id_admission_start_node = id_admission_start_node if id_admission_start_node else uuid.uuid4()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.admission_start_node (id_admission_start_node, code, name)
VALUES ('{self.id_admission_start_node}' :: UUID, '{self.code}', '{self.name}')
ON CONFLICT (code) DO NOTHING;"""


def generate_sql_file():
    df_admission_start_nodes = pd.read_csv("./AdmissionStartNode/admission_start_nodes.csv", encoding="utf-8")
    # Use only unique COD_NODE rows
    df_admission_start_nodes = df_admission_start_nodes.drop_duplicates(subset=['COD_NODO'])
    
    admission_start_nodes = [
        AdmissionStartNode(
            code=str(row['COD_NODO']),
            name=str(row['NODO'])
        )
        for _, row in df_admission_start_nodes.iterrows()
    ]
    
    with open("./AdmissionStartNode/admission_start_nodes.sql", "w", encoding="utf-8") as f:
        for admission_start_node in admission_start_nodes:
            f.write(admission_start_node.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")