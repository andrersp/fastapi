# -*- coding: utf-8 -*-

from pydantic import BaseModel, EmailStr


class Client(BaseModel):
    name: str
    email: EmailStr
    phone: str


class ClientInDB(Client):
    id: int
