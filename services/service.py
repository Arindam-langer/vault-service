from fastapi import HTTPException, status

from helper.crypto import encrypt_data, decrypt_data
from db.crud import create_token, get_token
from db.models import Token


def create_token_service(session, pii_data):
    try:
        token, token_id = encrypt_data(pii_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to encrypt PII data",
        )

    data = Token(
        token_id=token_id,
        ciphertext=token.ciphertext,
        auth_tag=token.auth_tag,
        iv=token.iv,
        key_version=token.key_version,
        encrypted_dek=token.encrypted_dek,
    )

    try:
        create_token(session, data)
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist token in database",
        )

    return {"tokenId": token_id}


def get_token_service(session, token_id):
    db_data = get_token(session, token_id)

    if db_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found",
        )

    token = Token(
        token_id=db_data.token_id,
        ciphertext=db_data.ciphertext,
        auth_tag=db_data.auth_tag,
        iv=db_data.iv,
        key_version=db_data.key_version,
        encrypted_dek=db_data.encrypted_dek,
    )

    try:
        pii_data = decrypt_data(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to decrypt token payload",
        )

    return {
        "token_id": token_id,
        "pii_data": pii_data,
    }
