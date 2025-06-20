import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class StudyPlanSubject:
    from typing import Optional
    def __init__(
        self,
        study_plan_code: str,
        subject_code: str,
        typology_code: str,
        id_study_plan_subject: Optional[uuid.UUID] = None
    ):
        if not study_plan_code or not subject_code or not typology_code:
            raise ValueError("StudyPlanSubject must have study_plan_code, subject_code, and typology_code")

        self.id_study_plan_subject = id_study_plan_subject or uuid.uuid4()
        self.study_plan_code = study_plan_code.strip()
        self.subject_code = subject_code.strip()
        self.typology_code = typology_code.strip()

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.study_plan_subject (
            id_study_plan_subject, id_study_plan, id_subject, id_typology
        ) VALUES (
            '{self.id_study_plan_subject}',
            (SELECT id_study_plan FROM {SCHEME_NAME_HA}.study_plan WHERE code = '{self.study_plan_code}'),
            (SELECT id_subject FROM {SCHEME_NAME_HA}.subject WHERE code = '{self.subject_code}'),
            (SELECT id_typology FROM {SCHEME_NAME_HA}.typology WHERE code = '{self.typology_code}')
        ) ON CONFLICT DO NOTHING;"""

