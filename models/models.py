from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class PII_data(BaseModel):
    name: str
    email: EmailStr
    phone_no: str = Field(pattern=r"^\d{10}$")
    ssn: str = Field(pattern=r"^\d{9}$")


class TokenColumn(str, Enum):
    CIPHERTEXT = "ciphertext"
    ENCRYPTED_DEK = "encrypted_dek"
    IV = "iv"
    AUTH_TAG = "auth_tag"
    KEY_VERSION = "key_version"
    REVOKED = "revoked"
