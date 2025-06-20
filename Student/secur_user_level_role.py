import uuid

class SecurUserLevelRole:
    def __init__(self, id: uuid.UUID, id_user: uuid.UUID, role_name: str, created_by: uuid.UUID, updated_by: uuid.UUID = None):
        self.id = id
        self.id_user = id_user
        self.role_name = role_name
        self.created_by = created_by
        self.updated_by = updated_by if updated_by else created_by

    def to_sql(self) -> str:
        return f"""INSERT INTO "security".secur_user_level_role (
            id_secur_user_level_role, id_secur_user, id_secur_role, created_by, updated_by
        ) VALUES (
            '{self.id}', '{self.id_user}', 
            (SELECT id_secur_role FROM "security".secur_role WHERE name = '{self.role_name}'),
            '{self.created_by}', '{self.updated_by}'
        );"""
