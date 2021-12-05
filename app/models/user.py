# -*- coding: utf-8 -*-

from sqlalchemy import Integer, String, Column, Boolean, event, Table, event, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from app.ext.database import metadata
from app.core.auth import get_password_hashed


user_roles = Table(
    'roles',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(20)),
    Column('role', String(40))
)


users_database = Table(
    'users',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('username', String(20), index=True),
    Column('full_name', String()),
    Column('email', String(100), index=True),
    Column('password', String(80), index=True),
    Column('enabled', Boolean(), default=False),
    Column('role_id', Integer, ForeignKey(user_roles.c.id))

)

# Create Fisrt User


@event.listens_for(user_roles, 'after_create')
def create_default_roles(target, connection, **kwargs):
    roles = [{
        "id": 1,
        'name': "Cliente",
        "role": "role:client"
    },
        {
        "id": 2,
        'name': "Operacional",
        "role": "role:operational"
    },
        {
        "id": 3,
        'name': "Administrador",
        "role": "role:admin"
    },
        {
        "id": 4,
        'name': "Developer",
        "role": "role:dev"
    }
    ]

    for role in roles:
        connection.execute("INSERT INTO roles (name, role) VALUES "
                           f"('{role.get('name')}', '{role.get('role')}')")


# Create Fisrt User
@event.listens_for(users_database, 'after_create')
def create_fist_user(target, connection, **kwargs):
    password = get_password_hashed('admin')
    connection.execute(
        "INSERT INTO users (username, email, password, enabled, role_id) "
        f"VALUES ('admin', 'email@mail.com', '{password}', True, 4)"
    )
