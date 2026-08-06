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

now i need to look at any refactors and ways to make a migration to postgres
#### TODO
add a migration to postgres.