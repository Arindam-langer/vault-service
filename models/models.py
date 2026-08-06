from enum import Enum
from typing import Any

from pydantic import RootModel


class PII_data(RootModel[dict[str, Any]]):
    pass


class TokenColumn(str, Enum):
    CIPHERTEXT = "ciphertext"
    ENCRYPTED_DEK = "encrypted_dek"
    IV = "iv"
    AUTH_TAG = "auth_tag"
    KEY_VERSION = "key_version"
    REVOKED = "revoked"
