# Vault Service
**Task:** to encrypt PII data and return a token
**tech things to sort**
so we need to containerize the postgres to store tokens and redis to implement  in case of reads.

i also wanna try rewritting microservices and compare there performance,
so first make it in python fast api then in go lang
and then share the metrics of each
## Some Basics:
so it goes like this we need a schema for now
so we need to containerize the postgres to store tokens and redis to implement  in case of reads.
# Vault Service
**Task:** to encrypt PII data and return a token

## Some Basics:
so it goes like this we need a schema for now
(PII)
email:
phone_No.:
name:
-------
(Non-PII)
user_id:
country:
user_status:
------
we divide the data into parts in two different DBs
one with PII data and one with non-PII
our main services work with the one with Non-PII
and when PII is needed to be get we just do a api call to that db and return raw

## Storing PII Data
it is more complicated then i thought since you need to make store it encrypted as well so schema becomes kinda tricky where you store the whole data in one column only,
i read with chatGPT that OKTA uses **AES-256-GCM**, which is a special type of encryption explained in its flow only. so we run the AES-256-GCM flow and store the cipher text, DEK(Data encryption key encrypted using the master key using some normal encryption), auth tag and return the tokenID that is generated as well.

### PII_DB Schema
Token_ID:
CipherText:
DEK:(random,encrypted)
IV:(random, raw)
Auth_Tag: from aes encryption
key_version: in-case we make changes in the master key

In normal terms:
1. Request arrives with PII (e.g. email)
2. Generate a random DEK for this record only
3. Generate a random IV (unique)
4. Run AES-256-GCM: (PII + DEK + IV) → ciphertext + auth_tag
5. Encrypt the DEK using the master key (from KMS/env) → encrypted_dek
6. Store: ciphertext, auth_tag, iv, encrypted_dek, key_version
7. Return a vault_id/token to the caller

#### Need to thinking about the case where we have to change the master key:
For example, we have Master_key_v1 now we have to change the key we just run the decryption and reencryption on the DEK since master_key just encrypts that which makes it very easy. think of it like a migration, where this flow happens, where we just reencrypt DEK with new key and nothing happens to cipher text 

#### AES-256-GCM
In simple terms, we get PII data like E-mail(xyz@xyzmail.com) now we have a 
**IV (Initialization vector)**, **random DEK(Data Encryption Key)**, our plain data the (E-mail,phoneNo. ),

When we get all three of them we use all of them into a function and we are returned two things:
- encrypted/cipher text
- and auth tag
we just store those in DB

in simple flow 
PII data + MasterKey(in the env) + DEK(random for every record) --> aes-256-GCM function == auth tag and cipher tag

``note: we need to make a comparison for **polymorphic encryption** and **AES-256-GCM**``


## Getting PII Data
We get a get api call requesting the data we encrypted, Now how do we do it , so here it goes,
for example we get a json like this: 
``
{
  "name": "Arindam Sen",
  "email": "arindam.sen@example.com",
  "phoneNumber": "+91-9876543210"
}
``
now how is it storing in the cipher text that is the biggest question which we get is how is the data we get 

## Main_DB
we know about what the PII db does what does the rest of the code does because i need it to show something which should be cooler than the PII i am implementing any suggestions
----

### Main_DB Schema
user_id:
country:
user_status:
token_ID: stores the tokenId recieved from the PII_DB
(PII)
email:
phone_No.:
name:
-------
(Non-PII)
user_id:
country:
user_status:
------
we divide the data into parts in two different DBs
one with PII data and one with non-PII
our main services work with the one with Non-PII
and when PII is needed to be get we just do a api call to that db and return raw

## Storing PII Data
it is more complicated then i thought since you need to make store it encrypted as well so schema becomes kinda tricky where you store the whole data in one column only,
i read with chatGPT that OKTA uses **AES-256-GCM**, which is a special type of encryption explained in its flow only. so we run the AES-256-GCM flow and store the cipher text, DEK(encrypted using the master key using some normal encryption), auth tag and return the tokenID that is generated as well.

### PII_DB Schema
Token_ID:
CipherText:
DEK:(random,encrypted)
IV:(random, raw)
Auth_Tag: from aes encryption
key_version: in-case we make changes in the master key

In normal terms:
1. Request arrives with PII (e.g. email)
2. Generate a random DEK for this record only
3. Generate a random IV (unique)
4. Run AES-256-GCM: (PII + DEK + IV) → ciphertext + auth_tag
5. Encrypt the DEK using the master key (from KMS/env) → encrypted_dek
6. Store: ciphertext, auth_tag, iv, encrypted_dek, key_version
7. Return a vault_id/token to the caller

#### Need to thinking about the case where we have to change the master key:
For example, we have Master_key_v1 now we have to change the key we just run the decryption and reencryption on the DEK since master_key just encrypts that which makes it very easy. think of it like a migration, where this flow happens, where we just reencrypt DEK with new key and nothing happens to cipher text 

#### AES-256-GCM
In simple terms, we get PII data like E-mail(xyz@xyzmail.com) now we have a 
**IV (Initialization vector)**, **random DEK(Data Encryption Key)**, our plain data the (E-mail,phoneNo. ),

When we get all three of them we use all of them into a function and we are returned two things:
- encrypted/cipher text
- and auth tag
we just store those in DB

in simple flow 
PII data + MasterKey(in the env) + DEK(random for every record) --> aes-256-GCM function == auth tag and cipher tag

``note: we need to make a comparison for **polymorphic encryption** and **AES-256-GCM**``


## Getting PII Data
We get a get api call requesting the data we encrypted, Now how do we do it , so here it goes,
for example we get a json like this: 
``
{
  "name": "Arindam Sen",
  "email": "arindam.sen@example.com",
  "phoneNumber": "+91-9876543210"
}
``
now how is it storing in the cipher text that is the biggest question which we get is how is the data we get 
i have added dynamic pii handling so we are gucci.

##### thinking of token revocation system
now the main question is how are we going to deal with master token changing.
so i have a shit ton of anxiety about this but this is so fucking cool,
okay so we have right now we are storing the master key and key ver in the env, but to make the master token dynamic we can just do this where we add new version in env and go as we do, but that is very inefficient and redundant and requires alot of human touching

well Arindam we just make a migration script you know which we run when we need to rotate the script, well gee, that is a great idea but what about the running traffic do we down the db, no we just make a new db and encrypt DEK(Data encryption key ) with new master key in the new db and complete until it is done but it is also very human interventiony, because the scope of this service has changed now, it is not single client(me), yeah i am changing to make it handle multiple clients and it is the users that rotate there master keys, which creates more questions on how to handle different client which we do after making this because generate token is constantly same working the part to onboard clients we need to go **multi tenant** but that is also different in thinking.

now **my solution** we store key in a key management system as KMS in which we store the master keys for every client.

now the thinking is api trigger of rotate causes the master token switch in KMS and start the migration, this will be for the case that client is already onboarded i dont wanna think of onboarding for now because that shit comes in **multi tenant** so now we store the master token in a kms but i dont know what is a kms just that it is a db that is storing the keys for each client. now for now we will store it in another table and then shift according to the mood,
the schema for a kms is

``` 
tenant_id
master key(encrypted)
key version
status: active | retiring | retired
rotationTriggered by: 
created date
retired date
```

found this : [KEY ENCRYPTION KEY (KEK) ROTATION FOR MULTI-TENANT (MT) SYSTEM](https://patents.justia.com/patent/20190173674)

so what i think can solve master key rotation flow, two guys are at play
  1. the key management system that stores client's keys
  2. how we do the changing of master key.

how we do the changing of master key?
this is a nice question but i have found a nice answer for this, let's explain it with an example:
for example we have company_A that has 1 million records in our vault that have a DEK encrypted with master key version: v1.0. So, its all good now like it is stored in our very secure KMS with the above schema !! so now a super user with admin role and access level token does the master token rotate now.
what happens?? first we update the old token version status to retiring. we generate a new master token and update the key version and append it to the record with the tenent id of that client and update the rest of the records, now we have a new key and a retiring key, and we return 200 that master key rotated, we can provide the master key but what is the client gonna do with it, nothing i guess so we just tell him which key version is now there master key is on.

now what happens after that api call to change the master token: a background job starts that runs for that tenent and starts to updates the DEKs, but we dont lock the db i have to study if the following thing will lock the db in case the record that is about to be updated is get at the same time or any other issue is caused like that or not.
now if the client sends a request to create a new token we are going to fetch the latest version and use that and encrypt the dek and move.
what about we get that token which uses old key version for dek, simple we just put a check that if the old key is used we update the decrypt the dek using the old key by fetching it from the kms with the keyversion stored in with that record and get the pii data then if that key is updating or in retiring state we just encrypt dek with the latest key version and update the record  and change the key version in the vault  db. and move on

the background still working and updating and when it ends we just update the status of "retiring" to "retired" and stop.

now what else can be the issue in the feature: 
what happens when two calls happen 

#### to do:
- i need to work on authn and authz
- audit logs on who revoked the token and who started token revocation 
i also need to find out what roles and policies each route needs.
