# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr, BaseModel
from typing import Optional, List

# from sqlalchemy.orm import relationship
# from sqlalchemy_serializer import SerializerMixin

from app.ext.database import async_session, engine, get_session

from sqlmodel import SQLModel, Column, String, Field, Relationship





class TokenStr(BaseModel):
    username: Optional[str] = None
    
class UseBase(SQLModel):
    username: str 
    password: str = Field(max_length=80)
    full_name: str
    email: EmailStr
    enabled: bool
    role_id: Optional[int] = Field(default=None, foreign_key='roles.id')    

class Users(UseBase, table=True):
    __tablename__ = 'user'
    id: Optional[int] = Field(default=None, primary_key=True)
    
    role: Optional['UserRole'] = Relationship(back_populates='user')

class UserUpdate(BaseModel):
    full_name: str
    email: EmailStr
    enabled: bool
    role_id: Optional[int] = Field(default=None, foreign_key='roles.id')  



class UserRole(SQLModel, table=True):
    __tablename__ = 'roles'
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=40)
    role: str = Field(max_length=40)
    user: List[Users] = Relationship(back_populates='role')

# class ModelUser(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     username = Column(String(40), index=True)
#     full_name = Column(String(40))
#     email = Column(String(40))
#     enabled = Column(Boolean(), default=True)

# user_roles = Table(
#     'roles',
#     metadata,
#     Column('id', Integer(), primary_key=True),
#     Column('name', String(20)),
#     Column('role', String(40))
# )


# users_database = Table(
#     'users',
#     metadata,
#     Column('id', Integer(), primary_key=True),
#     Column('username', String(20), index=True),
#     Column('full_name', String()),
#     Column('email', String(100), index=True),
#     Column('password', String(80), index=True),
#     Column('enabled', Boolean(), default=False),
#     Column('role_id', Integer, ForeignKey(user_roles.c.id))

# )

# Create Fisrt User


# @event.listens_for(user_roles, 'after_create')
# def create_default_roles(target, connection, **kwargs):
#     roles = [{
#         "id": 1,
#         'name': "Cliente",
#         "role": "role:client"
#     },
#         {
#         "id": 2,
#         'name': "Operacional",
#         "role": "role:operational"
#     },
#         {
#         "id": 3,
#         'name': "Administrador",
#         "role": "role:admin"
#     },
#         {
#         "id": 4,
#         'name': "Developer",
#         "role": "role:dev"
#     }
#     ]

#     for role in roles:
#         connection.execute("INSERT INTO roles (name, role) VALUES "
#                            f"('{role.get('name')}', '{role.get('role')}')")


# session = AsyncSession()
# # Create Fisrt User


    # password = get_password_hashed('vendas')
    # connection.execute(
    #     "INSERT INTO users (username, email, password, enabled, role_id) "
    #     f"VALUES ('vendas', 'vendas@mail.com', '{password}', True, 2)"
    # )

# event.listens_for(session, 'after_create', create_fist_user)