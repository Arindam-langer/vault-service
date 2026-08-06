import logging

from fastapi import HTTPException, status

from helper.crypto import encrypt_data, decrypt_data
from db.crud import create_token, get_token, update_token
from db.models import Token
from models.models import TokenColumn

logger = logging.getLogger(__name__)


def create_token_service(session, pii_data):
    try:
        token, token_id = encrypt_data(pii_data)
        logger.info(
            "Encrypted PII payload and generated token", extra={"token_id": token_id}
        )
    except Exception as exc:
        logger.exception("Encryption failed for PII payload")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to encrypt PII data",
        ) from exc

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
        logger.info("Persisted token to database", extra={"token_id": token_id})
    except Exception as exc:
        session.rollback()
        logger.exception(
            "Database persist failed for token", extra={"token_id": token_id}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist token in database",
        ) from exc

    return {"tokenId": token_id}


def get_token_service(session, token_id):
    db_data = get_token(session, token_id)

    if db_data is None:
        logger.warning("Token not found", extra={"token_id": token_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found",
        )
    if db_data.revoked is True:
        logger.warning("Attempt to access revoked token", extra={"token_id": token_id})
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Token is already revoked",
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
        logger.info("Decrypted token payload", extra={"token_id": token_id})
    except Exception as exc:
        logger.exception("Decryption failed for token", extra={"token_id": token_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to decrypt token payload",
        ) from exc

    return {
        "token_id": token_id,
        "pii_data": pii_data,
    }


def revoke_token_service(session, token_id):
    updated_token = update_token(
        session,
        token_id,
        column=TokenColumn.REVOKED,
        value=True,
    )

    if updated_token is None:
        logger.warning(
            "Token revoke failed because token does not exist",
            extra={"token_id": token_id},
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found",
        )

    logger.info("Token revoked", extra={"token_id": token_id})
    return {"message": f"token: {token_id} revoked successfully"}
