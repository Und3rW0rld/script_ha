import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class AcademicFilePeriod:
    from typing import Optional
    def __init__(self, id_academic_file_period: uuid.UUID, 
                 cumulative_period_enroll: int, period_gpa: float, cumulative_gpa: float, enrolled_credits: int,
                 studied_credits: int, approved_credits: int, cancelled_credits: int, failed_subjects: int,
                 mandatory_core: int, mandatory_field: int, elective: int, optional_core: int, leveling: int, 
                 optional_field: int, degree_project: int, total_credit_quota: int, additional_credit_quota: int,
                 available_credit_quota: int, study_credit_quota: int, dual_degree_credit_quota: int,
                 id_academic_file: Optional[str] = None, id_period: Optional[str] = None):
        self.id_academic_file_period = id_academic_file_period
        self.id_academic_file = id_academic_file
        self.id_period = id_period
        self.cumulative_period_enroll = cumulative_period_enroll
        self.period_gpa = period_gpa
        self.cumulative_gpa = cumulative_gpa
        self.enrolled_credits = enrolled_credits
        self.studied_credits = studied_credits
        self.approved_credits = approved_credits
        self.cancelled_credits = cancelled_credits
        self.failed_subjects = failed_subjects
        self.mandatory_core = mandatory_core
        self.mandatory_field = mandatory_field
        self.elective = elective
        self.optional_core = optional_core
        self.leveling = leveling
        self.optional_field = optional_field
        self.degree_project = degree_project
        self.total_credit_quota = total_credit_quota
        self.additional_credit_quota = additional_credit_quota
        self.available_credit_quota = available_credit_quota
        self.study_credit_quota = study_credit_quota
        self.dual_degree_credit_quota = dual_degree_credit_quota

    def to_sql(self) -> str:
        return f"""INSERT INTO {SCHEME_NAME_HA}.academic_file_period (
            id_academic_file_period, id_academic_file, id_period, cumulative_period_enroll, period_gpa, cumulative_gpa,
            enrolled_credits, studied_credits, approved_credits, cancelled_credits, failed_subjects, mandatory_core, 
            mandatory_field, elective, optional_core, leveling, optional_field, degree_project, total_credit_quota, 
            additional_credit_quota, available_credit_quota, study_credit_quota, dual_degree_credit_quota
        ) VALUES (
            '{self.id_academic_file_period}',
            ({self.id_academic_file} LIMIT 1),
            (SELECT id_period FROM {SCHEME_NAME_HA}.period WHERE code = '{self.id_period}' LIMIT 1),
            {self.cumulative_period_enroll}, {self.period_gpa}, {self.cumulative_gpa}, {self.enrolled_credits},
            {self.studied_credits}, {self.approved_credits}, {self.cancelled_credits}, {self.failed_subjects},
            {self.mandatory_core}, {self.mandatory_field}, {self.elective}, {self.optional_core}, {self.leveling},
            {self.optional_field}, {self.degree_project}, {self.total_credit_quota}, {self.additional_credit_quota},
            {self.available_credit_quota}, {self.study_credit_quota}, {self.dual_degree_credit_quota}
        ) ON CONFLICT DO NOTHING;"""


def generate_sql_file():
    df_academic_file_period = pd.read_csv("./AcademicFilePeriod/academic_file_period.csv", encoding="utf-8")
    academic_file_periods = []

    for _, row in df_academic_file_period.iterrows():

        hist_academica = str(row['HIST_ACADEMICA'])
        
        cod_plan = str(row['COD_PLAN'])

        hist_acad_select_id = f"SELECT id_academic_file FROM {SCHEME_NAME_HA}.academic_file WHERE code = '{hist_academica}' AND id_study_plan = (SELECT id_study_plan FROM {SCHEME_NAME_HA}.study_plan WHERE code = '{cod_plan}')"

        academic_file_periods.append(
            AcademicFilePeriod(
                id_academic_file_period=uuid.uuid4(),
                id_academic_file=hist_acad_select_id,
                id_period=str(row['PERIODO_ACADEMICO']),
                cumulative_period_enroll=int(row['NUM_MATRICULAS']) if pd.notna(row['NUM_MATRICULAS']) else 0,
                period_gpa=float(str(row['PAPA_PERIODO']).replace(",", ".")) if pd.notna(row['PAPA_PERIODO']) else 0.0,
                cumulative_gpa=float(str(row['PROM_ACADEMICO_ACTUAL']).replace(",", ".")) if pd.notna(row['PROM_ACADEMICO_ACTUAL']) else 0.0,
                enrolled_credits=int(row['CREDITOS_INSCRITOS_PER']) if pd.notna(row['CREDITOS_INSCRITOS_PER']) else 0,
                studied_credits=int(row['CRED_CURSADOS_PER']) if pd.notna(row['CRED_CURSADOS_PER']) else 0,
                approved_credits=int(row['CREDITOS_APROBADOS']) if pd.notna(row['CREDITOS_APROBADOS']) else 0,
                cancelled_credits=int(row['CREDITOS_CANCELADOS']) if pd.notna(row['CREDITOS_CANCELADOS']) else 0,
                failed_subjects=int(row['ASIG_REPROBADAS_PER']) if pd.notna(row['ASIG_REPROBADAS_PER']) else 0,
                mandatory_core=int(row['EXIGIDOS_C']) if pd.notna(row['EXIGIDOS_C']) else 0,
                mandatory_field=int(row['EXIGIDOS_B']) if pd.notna(row['EXIGIDOS_B']) else 0,
                elective=int(row['EXIGIDOS_T']) if pd.notna(row['EXIGIDOS_T']) else 0,
                optional_core=int(row['EXIGIDOS_O']) if pd.notna(row['EXIGIDOS_O']) else 0,
                leveling=int(row['EXIGIDOS_E']) if pd.notna(row['EXIGIDOS_E']) else 0,
                optional_field=int(row['EXIGIDOS_L']) if pd.notna(row['EXIGIDOS_L']) else 0,
                degree_project=int(row['EXIGIDOS_P']) if pd.notna(row['EXIGIDOS_P']) else 0,
                total_credit_quota=int(row['CREDITOS_PLAN']) if pd.notna(row['CREDITOS_PLAN']) else 0,
                additional_credit_quota=0, #no data available
                available_credit_quota=0, #no data available
                study_credit_quota=0, #no data available
                dual_degree_credit_quota=0
            )
        )
    
    with open("./AcademicFilePeriod/academic_file_period.sql", "w", encoding="utf-8") as f:
        for academic_file_period in academic_file_periods:
            f.write(academic_file_period.to_sql() + "\n")