# -*- coding: utf-8 -*-

from sqlalchemy import String, Column, Integer, Table

from app.ext.database import metadata


client_databse = Table(
    'client',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(40), index=True),
    Column('email', String(40), index=True),
    Column('phone', String(10))
)
