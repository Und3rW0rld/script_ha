import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA, CREATED_BY_UUID, DEFAULT_COUNTRY_ID, STUDENT_ROLE_NAME
import pandas as pd
from Student.secur_person import SecurPerson
from Student.student import Student
from Student.secur_user_level_role import SecurUserLevelRole
from Student.secur_user import SecurUser

def clean_text(value, max_length=None):
    if not value or pd.isna(value) or value in ["", "NULL", "None"]:
        return None
    value = str(value).strip()
    value = value.replace("'", "''")
    return value[:max_length] if max_length else value

def generate_sql_file():
    df_student = pd.read_csv("./Student/students.csv", encoding="utf-8")

    students = []
    users = []
    secur_people = []
    roles = []

    for _, row in df_student.iterrows():
        id_student = uuid.uuid4()
        legal_sex = str(row['SEXO_LEGAL']).strip() if pd.notna(row['SEXO_LEGAL']) else None
        if legal_sex and legal_sex.upper() == 'MASCULINO':
            legal_sex = 'M'
        elif legal_sex and legal_sex.upper() == 'FEMENINO':
            legal_sex = 'F'
        else:
            legal_sex = 'O'

        legal_id_type = str(row['TIPO_DOCUMENTO']).strip() if pd.notna(row['TIPO_DOCUMENTO']) else None
        if legal_id_type and legal_id_type.upper() == 'CÉDULA':
            legal_id_type = 'CC'
        elif legal_id_type and legal_id_type.upper() == 'TARJETA DE IDENTIDAD':
            legal_id_type = 'TI'
        elif legal_id_type and legal_id_type.upper() == 'PASAPORTE':
            legal_id_type = 'PAS'
        elif legal_id_type and legal_id_type.upper() == 'CÉDULA DE EXTRANJERÍA':
            legal_id_type = 'CE'
        else:
            legal_id_type = 'OT'
        
        username = str(row['USUARIO_INSTITUCIONAL']).strip() if pd.notna(row['USUARIO_INSTITUCIONAL']) else None
        
        if username:
            username = f"'{username}'"
        else:
            #ignorar registro si no tiene usuario institucional y guardar en un txt con la info de los student sin dicho usuario
            with open("./Student/students_without_username.txt", "a", encoding="utf-8") as f:
                f.write(f"ID: {id_student}, Legal ID Type: {legal_id_type}, Legal ID: {row['DOCUMENTO']}, Given Name: {row['NOMBRES_LEGAL']}, Surname: {row['APELLIDOS_LEGAL']}, Birth Date: {row['FECHA_NACIMIENTO']}, Legal Sex: {legal_sex}, Gender: {row['GENERO']}, Code: {row['CODIGO_INTERNO']}, Username: {username}, Institutional Email: {row['CORREO_INSTITUCIONAL']}\n")

            continue
        student = Student(
            id_student=id_student,
            legal_id_type=legal_id_type,
            legal_id=str(row['DOCUMENTO']),
            given_name=clean_text(str(row['NOMBRES_LEGAL'])),
            surname=clean_text(str(row['APELLIDOS_LEGAL'])),
            birth_date=row['FECHA_NACIMIENTO'] if pd.notna(row['FECHA_NACIMIENTO']) else None,
            legal_sex=legal_sex,
            gender=str(row['GENERO']),
            code=str(row['CODIGO_INTERNO']),
            username=username,
            institutional_email=str(row['CORREO_INSTITUCIONAL']),
            created_by=uuid.UUID(CREATED_BY_UUID),
            updated_by=uuid.UUID(CREATED_BY_UUID)
        )

        user = SecurUser(
                    id_user=id_student,
                    username=student.username,
                    email=student.institutional_email,
                    password="$2a$16$RoEWoIYViEk0wCftKS1G8u9c25hW0./I4B8ba6K49xH4usVcDGC9.",
                    created_by=uuid.UUID(CREATED_BY_UUID),
                    updated_by=uuid.UUID(CREATED_BY_UUID)
                )

        secur_person = SecurPerson(
            id_person=id_student,
            id_user=id_student,
            given_name=student.given_name if student.given_name else 'N/A',
            last_name=student.surname if student.surname else 'N/A',
            country_id=DEFAULT_COUNTRY_ID,
            legal_type_abbr=student.legal_id_type,
            legal_id=student.legal_id,
            birth_date=student.birth_date if student.birth_date else '1900-01-01',
            legal_gender_name=student.legal_sex,
            personal_email=student.institutional_email,
            created_by=uuid.UUID(CREATED_BY_UUID),
            updated_by=uuid.UUID(CREATED_BY_UUID)
        )

        role = SecurUserLevelRole(
                    id=uuid.uuid4(),
                    id_user=id_student,
                    role_name=STUDENT_ROLE_NAME,
                    created_by=uuid.UUID(CREATED_BY_UUID),
                    updated_by=uuid.UUID(CREATED_BY_UUID)
                )
        students.append(student)
        users.append(user)
        secur_people.append(secur_person)
        roles.append(role)
    
    with open("./Student/student.sql", "w", encoding="utf-8") as f:
        for student in students:
            f.write(student.to_sql())
    
    with open("./Student/secur_user.sql", "w", encoding="utf-8") as f:
        for user in users:
            f.write(user.to_sql())
    
    with open("./Student/secur_person.sql", "w", encoding="utf-8") as f:
        for secur_person in secur_people:
            f.write(secur_person.to_sql())
    
    with open("./Student/secur_user_level_role.sql", "w", encoding="utf-8") as f:
        for role in roles:
            f.write(role.to_sql())


if __name__ == "__main__":
    generate_sql_file()
    print("SQL files generated successfully.")