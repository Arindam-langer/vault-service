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

## Main_DB
we know about what the PII db does what does the rest of the code does because i need it to show something which should be cooler than the PII i am implementing any suggestions
----

### Main_DB Schema
user_id:
country:
user_status:
token_ID: stores the tokenId recieved from the PII_DB
