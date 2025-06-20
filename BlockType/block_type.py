import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class BlockType:
    def __init__(self, id_block_type: uuid.UUID, code: str, description: str):
        self.id_block_type = id_block_type
        self.code = code
        self.description = description

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.block_type (
            id_block_type, code, description
        ) VALUES (
            '{self.id_block_type}', '{self.code}', '{self.description}'
        ) ON CONFLICT DO NOTHING;"""
