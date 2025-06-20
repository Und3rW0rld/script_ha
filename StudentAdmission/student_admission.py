import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd


class StudentAdmission:
    def __init__(
        self,
        id_student,
        id_municipality,
        social_stratum,
        id_school_type,
        school_graduation_year,
        pbm,
        admission_score,
        total_standard_score,
        convocation,
        opening,
        id_admission_access,
        id_admission_subaccess,
        id_admission_start_node,
        id_study_plan,
        id_admission=None
    ):
        self.id_admission = id_admission or uuid.uuid4()
        self.id_student = id_student
        self.id_municipality = id_municipality
        self.social_stratum = social_stratum
        self.id_school_type = id_school_type
        self.school_graduation_year = school_graduation_year
        self.pbm = pbm
        self.admission_score = admission_score
        self.total_standard_score = total_standard_score
        self.convocation = convocation
        self.opening = opening
        self.id_admission_access = id_admission_access
        self.id_admission_subaccess = id_admission_subaccess
        self.id_admission_start_node = id_admission_start_node
        self.id_study_plan = id_study_plan
    def _fmt(self, value):
        if value is None or value == "":
            return "NULL"
        return str(value).replace(",", ".")  # importante si viene como str

    
    def to_sql(self):
        return f"""INSERT INTO {SCHEME_NAME_HA}.student_admission (
            id_student_admission, id_student, id_municipality, social_stratum,
            id_school_type, school_graduation_year, pbm, admission_score,
            total_standard_score, convocation, opening, id_admission_access,
            id_admission_subaccess, id_admission_start_node, id_study_plan
        ) VALUES (
            '{self.id_admission}', {self.id_student}, {self.id_municipality}, {self.social_stratum or 'NULL'},
            {self.id_school_type}, {self.school_graduation_year or 'NULL'}, {self._fmt(self.pbm)}, {self._fmt(self.admission_score)},
            {self._fmt(self.total_standard_score)}, '{self.convocation}', '{self.opening}', {self.id_admission_access},
            {self.id_admission_subaccess}, {self.id_admission_start_node}, {self.id_study_plan}
        ) ON CONFLICT DO NOTHING;"""

def generate_sql_file():
    df_student_admission = pd.read_csv("./StudentAdmission/student_admission.csv", encoding="utf-8")
    student_admissions = []
    #Iterar por el df con un bucle for
    for _, row in df_student_admission.iterrows():
        id_student = f"(SELECT id_student FROM {SCHEME_NAME_HA}.student WHERE code = '{row['CODIGO_INTERNO']}')"
        id_municipality = f"(SELECT id_municipality FROM {SCHEME_NAME_HA}.municipality WHERE code = '{row['COD_MUN_PROCEDENCIA']}')"
        tipo_colegio = row['MODACADEMICA'].strip()
        if tipo_colegio == 'No oficial':
            tipo_colegio = "PRV"
        else:
            tipo_colegio = "OFI"
        id_school_type = f"(SELECT id_school_type FROM {SCHEME_NAME_HA}.school_type WHERE name = '{tipo_colegio}')"
        id_access = f"(SELECT id_admission_access FROM {SCHEME_NAME_HA}.admission_access WHERE code = '{row['COD_ACCESO']}')"
        id_subaccess = f"(SELECT id_admission_subaccess FROM {SCHEME_NAME_HA}.admission_subaccess WHERE code = '{row['COD_SUBACCESO']}')" if row['COD_SUBACCESO'] else 'NULL'
        id_start_node = f"(SELECT id_admission_start_node FROM {SCHEME_NAME_HA}.admission_start_node WHERE code = '{row['NODO_INICIO']}')" if row['NODO_INICIO'] else 'NULL'
        id_study_plan = f"(SELECT id_study_plan FROM {SCHEME_NAME_HA}.study_plan WHERE code = '{row['COD_PLAN']}')"
        pbm = row['PBM_CALCULADO']
        if pd.isna(pbm):
            pbm = None
        puntaje_admision = row['PUNTAJE_ADMISION']
        if pd.isna(puntaje_admision):
            puntaje_admision = None
        
        ano_terminacion_colegio = row['ANO_TERMINACION_COLEGIO']
        if pd.isna(ano_terminacion_colegio):
            ano_terminacion_colegio = None

        student_admissions.append(
            StudentAdmission(
                id_student=id_student,
                id_municipality=id_municipality,
                social_stratum=row['ESTRATO'] if row['ESTRATO'] != "No Estratificado" and row['ESTRATO'] != "No Informa" else None,
                id_school_type=id_school_type,
                school_graduation_year=ano_terminacion_colegio,
                pbm=pbm,
                admission_score=puntaje_admision,
                total_standard_score=puntaje_admision,
                convocation=row['CONVOCATORIA'],
                opening=row['APERTURA'],
                id_admission_access=id_access,
                id_admission_subaccess=id_subaccess,
                id_admission_start_node=id_start_node,
                id_study_plan=id_study_plan
            )
        )

    with open("./StudentAdmission/student_admission.sql", "w", encoding="utf-8") as f:
        for student_admission in student_admissions:
            f.write(student_admission.to_sql())

if __name__ == "__main__":
    generate_sql_file()
    print("SQL file generated successfully.")
