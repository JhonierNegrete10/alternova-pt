from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class gender(Enum):
    male: str = "male"
    female: str = "female"


# User Model
class UserBase(BaseModel):
    username: str
    email: str


password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}$"


class UserLogin(BaseModel):
    email: str
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        regex=password_regex,
        description="Its a field with almost 8 character",
    )


# todo: change to userResponse
class UserOutput(UserBase):
    first_name: str
    last_name: str
    # username: str


class UserRegister(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
    )
    gender: gender
    phone: str = Field()
    email: EmailStr = Field(unique=True)


# Define modelo de base de datos SQLModel
class UserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    username: str
    email: str
    hashed_password: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    scopes: List[str] = []
