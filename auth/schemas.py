from enum import Enum
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    email: str
    username: str
    jetiq_username: str

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str
    jetiq_password: str


class UserUpdate(UserCreate):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    jetiq_username: Optional[str] = None
    jetiq_password: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class TokenType(str, Enum):
    BEARER = 'bearer'


class Token(BaseModel):
    access_token: str
    token_type: TokenType

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str] = None
