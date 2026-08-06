from fastapi import FastAPI
from models import PII_data, Encrypted_data
from encrypt import encrypt_data, create_token_id, decrypt_data

app = FastAPI()


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
async def read_token(token_id: str):
    db_data = Encrypted_data(**encrypted_data["cipher"])
    pii_data = decrypt_data(db_data)
    return {"token_id": token_id, "pii_data": pii_data}


# Encrypt PII data
@app.post("/vault")
async def add_token(pii_data: PII_data):
    # we encrypt the token and return token_id
    _, token_id = encrypt_data(pii_data)
    return {"tokenId": token_id}
