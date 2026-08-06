from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from models import PII_data
from encrypt import encrypt_data, decrypt_data
from db.database import create_db_and_tables
from db.database import get_session
from db.crud import create_token, Session, get_token
from db.models import Token


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# Health Check
@app.get("/health")
async def root():
    return {"status": "all good"}


# Get PII data
@app.get("/vault/{token_id}")
async def read_token(token_id: str, session: Session = Depends(get_session)):
    db_data = get_token(session=session, token_id=token_id)
    # fetch was successful
    token = Token(
        token_id=db_data.token_id,
        ciphertext=db_data.ciphertext,
        auth_tag=db_data.auth_tag,
        iv=db_data.iv,
        key_version=db_data.key_version,
        encrypted_dek=db_data.encrypted_dek,
    )
    pii_data = decrypt_data(token)
    return {"token_id": token_id, "pii_data": pii_data}


# Encrypt PII data
@app.post("/vault")
async def add_token(pii_data: PII_data, session: Session = Depends(get_session)):
    # we encrypt the token and return token_id
    token, token_id = encrypt_data(pii_data)
    data = Token(
        token_id=token_id,
        ciphertext=token.ciphertext,
        auth_tag=token.auth_tag,
        iv=token.iv,
        key_version=token.key_version,
        encrypted_dek=token.encrypted_dek,
    )
    create_token(session=session, data=data)
    return {"tokenId": token_id}
