import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class Student:
    def __init__(self, id_student, legal_id_type, legal_id, given_name, surname, birth_date,
                 legal_sex, gender, code, username, institutional_email, created_by, updated_by):
        self.id = id_student
        self.legal_id_type = legal_id_type
        self.legal_id = legal_id
        self.given_name = given_name
        self.surname = surname
        self.birth_date = birth_date
        self.legal_sex = legal_sex
        self.gender = gender
        self.code = code
        self.username = username
        self.institutional_email = institutional_email
        self.created_by = created_by
        self.updated_by = updated_by if updated_by else created_by

    def to_sql(self):
        birth = f"'{self.birth_date}'" if self.birth_date else "NULL"
        email = f"'{self.institutional_email}'" if self.institutional_email else "NULL"
        gender = f"'{self.gender}'" if self.gender else "NULL"
        return f"""
        INSERT INTO {SCHEME_NAME_HA}.student (
            id_student, legal_id_type, legal_id, given_name, surname,
            birth_date, legal_sex, gender, code, username, institutional_email,
            created_by, updated_by
        ) VALUES (
            '{self.id}', '{self.legal_id_type}', '{self.legal_id}',
            '{self.given_name}', '{self.surname}', {birth},
            '{self.legal_sex}', {gender}, '{self.code}', {self.username}, {email},
            '{self.created_by}', '{self.updated_by}'
        ) ON CONFLICT DO NOTHING;
        """