import uuid
from typing import Optional

class SecurUser:
    def __init__(self, id_user: uuid.UUID, password: str, email: str, created_by: uuid.UUID, updated_by: Optional[uuid.UUID] = None, username: Optional[str] = None):
        self.id_user = id_user
        self.username = username
        self.password = password  
        self.email = email
        self.created_by = created_by
        self.updated_by = updated_by if updated_by else created_by

    def to_sql(self) -> str:
        return f"""INSERT INTO "security".secur_user (
            id_secur_user, username, "password", email, created_by, updated_by
        ) VALUES (
            '{self.id_user}', {self.username}, '{self.password}', '{self.email}',
            '{self.created_by}', '{self.updated_by}'
        ) ON CONFLICT (email) DO NOTHING;"""
