# -*- coding: utf-8 -*-

from sqlalchemy import Integer, String, Column, Boolean, event
from sqlalchemy_serializer import SerializerMixin

from app.ext.database import Base


class ModelUser(Base, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), index=True)
    full_name = Column(String(), index=True)
    email = Column(String(100))
    password = Column(String(80))
    enabled = Column(Boolean, default=False)
