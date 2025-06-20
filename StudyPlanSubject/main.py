import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd

from StudyPlanSubject.study_plan_subject import StudyPlanSubject
from StudyPlanSubject.study_plan_subject_period import StudyPlanSubjectPeriod

def clean_text(value, max_length=None):
    if not value or pd.isna(value) or value in ["", "NULL", "None"]:
        return None
    value = str(value).strip()
    value = value.replace("'", "''")
    return value[:max_length] if max_length else value

def limit_text_to_length(text: str, length: int = 40) -> str:
    """Limit the text to a specified length."""
    if not text:
        return text
    text = text.strip()
    if len(text) > length:
        return text[:length] 
    return text

def generate_sql_file():
    df_study_plan_subject = pd.read_csv("./StudyPlanSubject/subjects.csv", encoding="utf-8")
    df_subject_period = pd.read_csv("./StudyPlanSubject/subject_period.csv", encoding="utf-8")

    dict_data = dict()

    # quiero que el diccionario guarde la info así key = {COD_ASIGNATURA, PERIODO} value = {GRUPO_ACTIVI}

    for _, row in df_subject_period.iterrows():
        key = (str(row['COD_ASIGNATURA']), str(row['PERIODO']))

        if pd.notnull(row['GRUPO_ACTA']):
            grupo_asignatura = str(int(row['GRUPO_ACTA']))
        else:
            
            grupo_asignatura = str(row['GRUPO_ACTIVI']).strip().split("Grupo ")[-1]
            if grupo_asignatura.isdigit():
                grupo_asignatura = str(int(grupo_asignatura))
            else:
                grupo_asignatura = None
            
        value = {
            'GRUPO_ACTIVIDAD': str(row['GRUPO_ACTIVI']),
            'ACTIVIDAD': str(row['ACTIVIDAD']),
            'PRINCIPAL': str(row['FLAG_PRINCIPAL']),
            'GRUPO_ASIGNATURA': grupo_asignatura 
        }
        if key not in dict_data:
            dict_data[key] = []
        dict_data[key].append(value)

    study_plan_subjects = []
    study_plan_subject_periods = []

    for _, row in df_study_plan_subject.iterrows():
        id_study_plan_subject = uuid.uuid4()
        study_plan_subjects.append(
            StudyPlanSubject(
                study_plan_code=str(row['PLA_CODALF']),
                subject_code=str(row['COD_ASIG']),
                typology_code=str(row['TIPOLOGIA']),
                id_study_plan_subject=id_study_plan_subject
            )
        )
        data = dict_data.get((str(row['COD_ASIG']), str(row['PERIODO_ASIG_NUM'])), [])
        study_plan_subject_periods.append(
            StudyPlanSubjectPeriod(
                id_study_plan_subject_period=uuid.uuid4(),
                id_study_plan_subject=id_study_plan_subject,
                code_period=clean_text(str(row['PERIODO_ASIG_NUM'])),
                subject_group=clean_text(limit_text_to_length(data[0]['GRUPO_ASIGNATURA'])) if data else None,
                activity_group=clean_text(limit_text_to_length(data[0]['GRUPO_ACTIVIDAD'])) if data else None,
                activity=clean_text(limit_text_to_length(data[0]['ACTIVIDAD'])) if data else None,
                principal_activity=clean_text(limit_text_to_length(data[0]['PRINCIPAL'])) if data else None
            )
        )

    df_study_plan_subject_2 = pd.read_csv("./StudyPlanSubject/subjects2.csv", encoding="utf-8")

    for _, row in df_study_plan_subject_2.iterrows():
        id_study_plan_subject = uuid.uuid4()
        study_plan_subjects.append(
            StudyPlanSubject(
                study_plan_code=str(row['PLA_CODALF']),
                subject_code=str(row['COD_ASIG']),
                typology_code=str(row['TIPOLOGIA']),
                id_study_plan_subject=id_study_plan_subject
            )
        )
        data = dict_data.get((str(row['COD_ASIG']), str(row['PERIODO_ASIG_NUM'])), [])
        study_plan_subject_periods.append(
            StudyPlanSubjectPeriod(
                id_study_plan_subject_period=uuid.uuid4(),
                id_study_plan_subject=id_study_plan_subject,
                code_period=clean_text(limit_text_to_length(str(row['PERIODO_ASIG_NUM']))),
                subject_group=clean_text(limit_text_to_length(data[0]['GRUPO_ASIGNATURA'])) if data else None,
                activity_group=clean_text(limit_text_to_length(data[0]['GRUPO_ACTIVIDAD'])) if data else None,
                activity=clean_text(limit_text_to_length(data[0]['ACTIVIDAD'])) if data else None,
                principal_activity=clean_text(limit_text_to_length(data[0]['PRINCIPAL'])) if data else None
            )
        )


    with open("./StudyPlanSubject/study_plan_subject.sql", "w", encoding="utf-8") as f:
        for study_plan_subject in study_plan_subjects:
            f.write(study_plan_subject.to_sql())
    
    with open("./StudyPlanSubject/study_plan_subject_period.sql", "w", encoding="utf-8") as f:
        for study_plan_subject_period in study_plan_subject_periods:
            f.write(study_plan_subject_period.to_sql() + "\n")

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")