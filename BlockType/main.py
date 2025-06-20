import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

from BlockType.academic_file_block import AcademicFileBlock
from BlockType.block_type import BlockType
from AcademicFilePeriod.academic_file_period import AcademicFilePeriod

def parse_date(date_str):
    if date_str:
        return str(date_str).split()[0]  
    return None

def generate_sql_file():

    df_block_type = pd.read_csv("./BlockType/block_type.csv", encoding="utf-8")

    dict_data = dict()

    df_academic_file_period = pd.read_csv("./AcademicFilePeriod/academic_file_period.csv", encoding="utf-8")
    academic_file_periods = []

    for _, row in df_academic_file_period.iterrows():

        id_academic_file_period = uuid.uuid4()

        dni_student = str(row['DOCUMENTO'])
        if dni_student not in dict_data:
            dict_data[dni_student] = {
                'id_academic_file_period': id_academic_file_period,
            }

        hist_academica = str(row['HIST_ACADEMICA'])
        
        cod_plan = str(row['COD_PLAN'])

        hist_acad_select_id = f"SELECT id_academic_file FROM {SCHEME_NAME_HA}.academic_file WHERE code = '{hist_academica}' AND id_study_plan = (SELECT id_study_plan FROM {SCHEME_NAME_HA}.study_plan WHERE code = '{cod_plan}')"

        academic_file_periods.append(
            AcademicFilePeriod(
                id_academic_file_period=id_academic_file_period,
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
    
    df_block_type = pd.read_csv("./BlockType/block_type.csv", encoding="utf-8")

    block_types = []

    for _, row in df_block_type.iterrows():
        id_block_type = uuid.uuid4()
        block_type = BlockType(
            id_block_type=id_block_type,
            code=str(row['CODIGO']),
            description=str(row['DESCRIPCION'])
        )
        block_types.append(block_type)

    with open("./BlockType/block_type.sql", "w", encoding="utf-8") as f:
        for block_type in block_types:
            f.write(block_type.to_sql() + "\n")

    df_academic_file_block = pd.read_csv("./BlockType/block.csv", encoding="utf-8")
    academic_file_blocks = []
    for _, row in df_academic_file_block.iterrows():
        id_academic_file_block = uuid.uuid4()
        dni_student = str(row['ALU_DNIALU'])
        if dni_student in dict_data:
            id_academic_file_period = dict_data[dni_student]['id_academic_file_period']
        else:
            # Skip or handle missing academic_file_period for this student
            id_academic_file_period = None
        id_block_type = f"SELECT id_block_type FROM {SCHEME_NAME_HA}.block_type WHERE code = '{row['CODNUM']}' AND description = '{row['BLOQUEO']}'"
        block_date = str(row['FECHA_BLOQUEO'])
        is_active = True if row['BLO_ACT'] == 'S' else False

        academic_file_blocks.append(
            AcademicFileBlock(
                id_academic_file_block=id_academic_file_block,
                id_academic_file_period=id_academic_file_period,
                id_block_type=id_block_type,
                block_date=parse_date(block_date),
                is_active=is_active
            )
        )
    
    with open("./BlockType/academic_file_block.sql", "w", encoding="utf-8") as f:
        for academic_file_block in academic_file_blocks:
            f.write(academic_file_block.to_sql() + "\n")
    
if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")
