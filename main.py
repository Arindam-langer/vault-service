from fastapi import FastAPI,Depends
from models import PII_data, Encrypted_data
from encrypt import encrypt_data,decrypt_data
from db.database import create_db_and_tables
from db.database import get_session
from db.crud import create_token,Session,get_token
from db.models import Token

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

encrypted_data = {
    "cipher": {
        "ciphertext": "43gl4HOaVUE26NaqsxW5F3fPdQ3M2m6NlhZcHzGjuyBKyeSSbmExnor8KA+wZRoNNNwdvlROGiKSC4XiVzeh4gmbwuRZGGW4WMR3Jf17BAiDqb8zL0pGDDsu9A==",
        "auth_tag": "4J/dTz35Q0r7JfD7tAIbyg==",
        "iv": "FU2LrMOr3TI+hlCZ",
        "dek": "o/JM80mho1ieqNkAiXkuCEhT0e5RSME8YIFsp57biX8/SJ5f46s1Ww==",
        "key_version": "1.0",
    },
    "tokenId": "token_c9f9a120-1a2a-48f9-96fa-ae9e2c76eb4a",
}


# Health Check
@app.get("/health")
async def root():
    return {"status": "all good"}  # this considered is json


# Get PII data
@app.get("/vault/{token_id}")
async def read_token(token_id: str,session: Session = Depends(get_session)):
    db_data = get_token(session=session,token_id=token_id)
    # fetch was successful
    print("DEBUG:",db_data)
    token = Encrypted_data(
        ciphertext=db_data.ciphertext,
        auth_tag=db_data.auth_tag,
        iv=db_data.iv,
        key_version=db_data.key_version,
        dek=db_data.encrypted_dek,
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
        encrypted_dek=token.dek,
    )
    create_token(session=session,data=data)
    return {"tokenId": token_id}
