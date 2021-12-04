# -*- coding: utf-8 -*-

from sqlalchemy import Integer, String, Column, Boolean, event, Table, event
from sqlalchemy_serializer import SerializerMixin

from app.ext.database import metadata
from app.core.auth import get_password_hashed


users_database = Table(
    'users',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('username', String(20), index=True),
    Column('full_name', String()),
    Column('email', String(100), index=True),
    Column('password', String(80), index=True),
    Column('enabled', Boolean(), default=False)

)


# Create Fisrt User
@event.listens_for(users_database, 'after_create')
def create_fist_user(target, connection, **kwargs):
    password = get_password_hashed('admin')
    connection.execute(
        "INSERT INTO users (username, email, password, enabled) "
        f"VALUES ('admin', 'email@mail.com', '{password}', True)"
    )
