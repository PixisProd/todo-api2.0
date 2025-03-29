from pydantic import BaseModel, Field, EmailStr


class UserRegistration(BaseModel):
    login: str = Field(min_length=5, max_length=12, examples=["pixie25"])
    password: str = Field(min_length=5, max_length=20, examples=["Trixp256"])
    name: str = Field(min_length=3, max_length=12, examples=["Spike"])
    email: EmailStr = Field(examples=["pixistheprotector@gmail.com"])
