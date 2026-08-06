from sqlmodel import SQLModel, Field

class Token(SQLModel, table=True):
    token_id: str = Field(primary_key=True, index=True)
    ciphertext: str
    encrypted_dek: str
    iv: str
    auth_tag: str
    key_version: str