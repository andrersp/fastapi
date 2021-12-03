# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    username: str = Field(min_length=2)
    email: EmailStr
    full_name: Optional[str]
    enabled: Optional[bool]


class UserInDB(User):
    password: str = Field(min_length=6)

    # class Config:
    #     orm_mode = True


class UserResponse(User):
    id: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    email: Optional[str] = ""
    username: str
