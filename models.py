from pydantic import BaseModel

class PII_data(BaseModel):
    name: str
    email: str | None = None #add vaildation for valid email Must do
    phone_no: int #add validation for phoneNo. if needed i think 10 length
    ssn: int
