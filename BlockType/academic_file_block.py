import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class AcademicFileBlock:
    from typing import Optional
    def __init__(self, id_academic_file_block: uuid.UUID, 
                 id_block_type: str, is_active: bool, id_academic_file_period: Optional[uuid.UUID], block_date: Optional[str] = None):
        self.id_academic_file_block = id_academic_file_block 
        self.id_academic_file_period = f"'{id_academic_file_period}' :: UUID" if id_academic_file_period else "NULL"
        self.id_block_type = id_block_type
        self.block_date = block_date if block_date else "NULL"
        self.is_active = is_active

    def to_sql(self) -> str:
        block_date_parsed = self.block_date.replace('/', '-')
        return f"""INSERT INTO {SCHEME_NAME_HA}.academic_file_block (
            id_academic_file_block, id_academic_file_period, id_block_type, block_date, is_active
        ) VALUES (
            '{self.id_academic_file_block}' :: UUID, 
            {self.id_academic_file_period}, 
            ({self.id_block_type}), 
            '{block_date_parsed}' :: DATE, 
            {self.is_active}
        ) ON CONFLICT DO NOTHING;"""