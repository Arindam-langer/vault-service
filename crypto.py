import os
import uuid
import base64
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.keywrap import aes_key_wrap
from cryptography.hazmat.primitives.keywrap import aes_key_unwrap
from db.models import Token
from models.models import PII_data
from dotenv import load_dotenv

# env variables
load_dotenv()
key_ver = os.getenv("KEY_VERSION")
master_key = base64.b64decode(os.getenv("MASTER_KEY"))


def encrypt_data(data: PII_data):
    token_id = create_token_id()
    plaintext = json.dumps(data.model_dump()).encode("utf-8")
    dek = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(dek)
    iv = os.urandom(12)
    encrypted = aesgcm.encrypt(iv, plaintext, None)
    ciphertext = encrypted[:-16]
    auth_tag = encrypted[-16:]
    encrypted_dek = aes_key_wrap(master_key, dek)
    encrypted_data = Token(
        token_id=token_id,
        ciphertext=base64.b64encode(ciphertext).decode("ascii"),
        auth_tag=base64.b64encode(auth_tag).decode("ascii"),
        iv=base64.b64encode(iv).decode("ascii"),
        encrypted_dek=base64.b64encode(encrypted_dek).decode("ascii"),
        key_version=key_ver,
    )
    print(encrypted_data)
    # store the encrypted data in db
    # return just success or error or a token id here
    return encrypted_data, token_id


def create_token_id():
    id = str(uuid.uuid4())
    token_id = f"token_{id}"
    return token_id


def decrypt_data(token: Token):
    ciphertext = base64.b64decode(token.ciphertext)
    auth_tag = base64.b64decode(token.auth_tag)
    iv = base64.b64decode(token.iv)
    encrypted_dek = base64.b64decode(token.encrypted_dek)
    dek = aes_key_unwrap(master_key, encrypted_dek)
    encrypted = ciphertext + auth_tag
    aesgcm = AESGCM(dek)
    plaintext = aesgcm.decrypt(iv, encrypted, None)
    pii = json.loads(plaintext.decode("utf-8"))
    validate_pii = PII_data.model_validate(pii)

    return validate_pii
