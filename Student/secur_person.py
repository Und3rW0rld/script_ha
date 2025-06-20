import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import SCHEME_NAME_HA
import pandas as pd

class SecurPerson:
    from typing import Optional
    def __init__(self, id_person: uuid.UUID, id_user: uuid.UUID, given_name: str, last_name: str,
                country_id: int, legal_type_abbr: str, legal_id: str, birth_date: str, legal_gender_name: str,
                personal_email: str, created_by: uuid.UUID, updated_by: Optional[uuid.UUID] = None):
        self.id_person = id_person
        self.id_user = id_user
        self.given_name = given_name
        self.last_name = last_name
        self.country_id = country_id
        self.legal_type_abbr = legal_type_abbr
        self.legal_id = legal_id
        self.birth_date = birth_date
        self.legal_gender_name = legal_gender_name
        self.personal_email = personal_email
        self.created_by = created_by
        self.updated_by = updated_by if updated_by else created_by

    def to_subquery_sql(self) -> str:
        return f"""SELECT
            '{self.id_person}'::uuid AS id_secur_person,
            '{self.id_user}'::uuid AS id_secur_user,
            '{self.given_name}' AS given_name,
            '{self.last_name}' AS last_name,
            {self.country_id} AS id_locat_country,
            ct.id_trans_type_legal_id,
            '{self.legal_id}' AS legal_id,
            '{self.birth_date}'::DATE AS birth_date,
            cg.id_trans_legal_gender,
            '{self.personal_email}' AS personal_email,
            TRUE AS is_active,
            '{self.created_by}'::uuid AS created_by,
            '{self.updated_by}'::uuid AS updated_by
        FROM cached_types ct
        LEFT JOIN cached_genders cg ON cg.name = '{self.legal_gender_name}'
        WHERE ct.abbreviation = '{self.legal_type_abbr}'
    """

    def to_sql(self) -> str:
        return f"""INSERT INTO "security".secur_person (
            id_secur_person, id_secur_user, given_name, last_name, id_locat_country,
            id_trans_type_legal_id, legal_id, birth_date, id_trans_legal_gender,
            personal_email, is_active, created_by, updated_by
        ) VALUES (
            '{self.id_person}', '{self.id_user}', '{self.given_name}', '{self.last_name}', {self.country_id},
            (SELECT id_trans_type_legal_id FROM transversal.trans_type_legal_id WHERE abbreviation = '{self.legal_type_abbr}'),
            '{self.legal_id}', '{self.birth_date}'::DATE, 
            (SELECT id_trans_legal_gender FROM transversal.trans_legal_gender WHERE name = '{self.legal_gender_name}'),
            '{self.personal_email}', TRUE, '{self.created_by}', '{self.updated_by}'
        );"""
