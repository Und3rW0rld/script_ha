import uuid
from constants import SCHEME_NAME_HA

class AcademicFileRecord:
    def __init__(self, id_academic_file_record: uuid.UUID, id_academic_file_period: uuid.UUID, 
                 id_study_plan_subject_period: uuid.UUID, ind: str, record_type: str, alphabetical_score: str, 
                 score: float, cancelled: str, blocked: str, closed: str, with_academic_validity: str, 
                 total_study_times: int):
        self.id_academic_file_record = id_academic_file_record
        self.id_academic_file_period = id_academic_file_period
        self.id_study_plan_subject_period = id_study_plan_subject_period
        self.ind = ind
        self.record_type = record_type
        self.alphabetical_score = alphabetical_score
        self.score = score
        self.cancelled = cancelled
        self.blocked = blocked
        self.closed = closed
        self.with_academic_validity = with_academic_validity
        self.total_study_times = total_study_times

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.academic_file_record (
            id_academic_file_record, id_academic_file_period, id_study_plan_subject_period, ind, record_type, 
            alphabetical_score, score, cancelled, blocked, closed, with_academic_validity, total_study_times
        ) VALUES (
            '{self.id_academic_file_record}'::uuid, 
            (SELECT id_period FROM {SCHEME_NAME_HA}.period WHERE code = '{self.id_academic_file_period}'), 
            '{self.id_study_plan_subject_period}' ::uuid, 
            '{self.ind}', 
            '{self.record_type}', 
            '{self.alphabetical_score}', 
            {self.score}, 
            '{self.cancelled}', 
            '{self.blocked}', 
            '{self.closed}', 
            '{self.with_academic_validity}', 
            {self.total_study_times}
        ) ON CONFLICT DO NOTHING;"""
