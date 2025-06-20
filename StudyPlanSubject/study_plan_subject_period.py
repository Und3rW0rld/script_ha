import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd
from typing import Optional

class StudyPlanSubjectPeriod:
    def __init__(
        self,
        id_study_plan_subject_period: Optional[uuid.UUID] = None,
        id_study_plan_subject: Optional[uuid.UUID] = None,
        code_period: Optional[str] = None,
        subject_group: Optional[str] = None,
        activity_group: Optional[str] = None,
        activity: Optional[str] = None,
        principal_activity: Optional[str] = None
    ):
        self.id_study_plan_subject_period = id_study_plan_subject_period
        self.id_study_plan_subject = id_study_plan_subject
        self.code_period = code_period
        self.subject_group = subject_group
        self.activity_group = activity_group
        self.activity = activity
        self.principal_activity = principal_activity

    def to_sql(self) -> str:
        # Escapar posibles comillas simples en los valores
        def escape_string(value):
            return value.replace("'", "''") if value else value
        
        return f"""INSERT INTO {SCHEME_NAME_HA}.study_plan_subject_period (
            id_study_plan_subject_period, id_study_plan_subject, id_period, subject_group, activity_group, activity, principal_activity
        ) VALUES (
            '{self.id_study_plan_subject_period}', '{self.id_study_plan_subject}', 
            ( SELECT id_period FROM {SCHEME_NAME_HA}.period WHERE code = '{escape_string(self.code_period)}'), 
            '{escape_string(self.subject_group)}', '{escape_string(self.activity_group)}', 
            '{escape_string(self.activity)}', '{escape_string(self.principal_activity)}'
        ) ON CONFLICT DO NOTHING;"""