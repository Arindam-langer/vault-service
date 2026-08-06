from pydantic import BaseModel, EmailStr, Field


class PII_data(BaseModel):
    name: str
    email: EmailStr
    phone_no: str = Field(pattern=r"^\d{10}$")
    ssn: str = Field(pattern=r"^\d{9}$")
