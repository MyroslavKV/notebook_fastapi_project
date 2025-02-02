from typing import Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict
import enum


class UserType(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class InputUserData(BaseModel):
    username: str = Field(min_length=4)
    email: EmailStr
    password: str = Field(min_length=6)
    password_repeat: str = Field(min_length=6)
    role: UserType = UserType.USER

    @model_validator(mode="after")
    @classmethod
    def valid_pass(cls, data: Any):
        if data.password != data.password_repeat:
            raise ValueError("passwords not match")
        return data


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: UserType = UserType.USER
    bio: Optional[str] = Field(None)

    create_data: datetime = Field(datetime.now())


class ListBaseUsers(BaseModel):
    users: list[UserBase | None]
    count_users: int


class InputUpdateUser(BaseModel):
    username: Optional[str] = Field(None)
    bio: Optional[str] = None


class OutUserName(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str

class FullUserBase(UserBase):
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class NoteCreate(BaseModel):
    title: str = Field(..., max_length=255, description="Заголовок нотатки")
    content: str = Field(..., description="Вміст нотатки")


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255, description="Оновлений заголовок нотатки")
    content: Optional[str] = Field(None, description="Оновлений вміст нотатки")


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int

    class Config:
        from_attributes = True


class NotesList(BaseModel):
    notes: List[NoteResponse]
    count: int