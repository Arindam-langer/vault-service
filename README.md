To make a vault tech first of all i have never used fast api so what i would do right now is just make a server 
i will use uv
and just make a health checkpoint. just that for now
so step or phase 1 is just setup and making one end point.

made the health checkpoint so its all good and easy now i need to make a design of what the end points are going to be in this service.
so 
GET /vault/tokenId get the token data in decrypted form 
POST /vault add the token to db in encrypted
DELETE /vault delete or revoke that token, for which use case i dont know 
some batch detoken and add as well but i dont know the case for this
Admin endpoints (audit, key rotation, etc.).

If you have a path operation that receives a path parameter,
but you want the possible valid path parameter values to be predefined, you can use a standard Python Enum.
refer to https://fastapi.tiangolo.com/tutorial/path-params/#create-an-enum-class

for request body in fast api
https://fastapi.tiangolo.com/tutorial/body/#declare-it-as-a-parameter


well made the encryption and decryption functions they are working correctly now i am going to make now i am going to make it connect to db and we will go from there i guess
now how do you connect db in fastapi
well completed it, turns out it is very easy.
now we can fetch the decrypted token and add the pii data safely.

now i need to look at any refactors and ways to make a migration to postgres when i complete it
i am reading the code and i see that token class and Encrypted_data are very similar to each other just a difference of a token Id is there i think we can make it one only
i just did the greatest thing when i made update token!! function during the task of token revokation flow, i am the greatest dev to think it on the fly. thanks go lang patterns

- i am so **cracked** that for even development i am using openssl to create passwords
command: ``openssl rand -hex 16``
**Token Revocation Endpoint**:
  - *Reasoning*: Regulatory compliance (GDPR Right-to-be-forgotten / CCPA) requires services to revoke and hard-delete or mark tokens invalid upon request. 
    - TODO: make a cronjob to delete every token where revoked == true.
  - *How to solve this*: To solve this we just add a bool flag to revoke that token then make a cron job that clears the db of revoke=true tokens.


- Master Key Rotation Engine: how does this work???? that is the question???
so it is supposed to be a huge migration, i guess we are just changing the key version that encrypts dek, it should happen on an api call but since we can consider it a migration what we can do is make new migration table that does the copy of data and store it there, and then we clear that database.
we can go eventual consistency route where from the secrets use the master key accordingly  and get according to that until token revoked making it dynamic and change it in post with different key version.
so we get master key according to version and post according to new token. 

Database schema and data migrations from sqlite to post gres using alembic which is a industry standard but you need to make the changes apparently and make data migrations. a to do one more is going to run data migrations when i change the schema after this is completed 
**According to ai this is what i should implement now that i have completed basic stuff**
#### TODO 
- [x] **Support Dynamic PII Schemas**:
  - *Reasoning*: Hardcoding specific PII fields (`name`, `email`, `phone_no`, `ssn`) limits the vault's utility. A production vault accepts any JSON payload (`Dict[str, Any]`), encrypting whatever PII structure caller microservices send.
  - *How to solve this*: just make the pydantic model just validate if its json or not and done. thank you abstraction. you helped me.
- [x] **PostgreSQL Containerization & Migration**:
  - *Reasoning*: SQLite is single-file and lock-bound, unsuitable for high-throughput distributed microservices. Update `DATABASE_URL` to PostgreSQL and add DB connection pooling.
- [ ] **Redis Read Caching** (add it later):
  - *Reasoning*: Vault read operations (`GET /vault/{token_id}`) dominate write operations in real-world microservices. Caching decrypted/encrypted entries in Redis dramatically reduces database IOPS.
- [ ] **Docker Compose Setup**(add it before redis)):
  - *Reasoning*: Provide a unified `docker-compose.yml` spinning up FastAPI, PostgreSQL, and Redis with healthchecks and automatic migrations.
- [ ] **Master Key Rotation Engine (`POST /admin/rotate-key`)**:
  - *Reasoning*: AES-256-GCM envelope encryption allows rotating the Master Key by only re-wrapping the `encrypted_dek` column using `aes_key_wrap(new_master_key, unwrapped_dek)`—without touching or re-encrypting the payload ciphertext!
- [ ] **Key Version Tracking**:
  - *Reasoning*: Multi-version key support allows decrypting legacy tokens with older master keys while re-encrypting DEKs during background key migration.
- [ ] **Batch Tokenization & Detokenization (`POST /vault/batch`)**:
  - *Reasoning*: Prevents N+1 HTTP calls when microservices handle bulk data pipelines.
- [ ] **Go Language Port & Performance Comparison**:
  - *Reasoning*: As outlined in `vault design.md`, rewrite core endpoints in Go (using `crypto/cipher` AES-GCM and `pgx`) and benchmark Python FastAPI vs. Go using `k6` or `wrk` under high concurrency.
