from pydantic import BaseModel, EmailStr
from enum import Enum

class UserType(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: str = ""

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: UserType

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
