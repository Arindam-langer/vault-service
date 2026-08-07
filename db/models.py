from sqlmodel import SQLModel, Field
from models.models import KeyStatus


class Token(SQLModel, table=True):
    token_id: str = Field(primary_key=True, index=True)
    ciphertext: str
    encrypted_dek: str
    iv: str
    auth_tag: str
    key_version: str
    revoked: bool = Field(default=False)


# TODO: change it to a KMS(Key Management System)
class KeyVersions(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tenant_id: str
    key_version: str
    encrypted_master_key: str
    status: KeyStatus
