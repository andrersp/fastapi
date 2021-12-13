# -*- coding: utf-8 -*-
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from app.models.user import Users, UseBase
from app.ext.database import async_session, get_session

# async def authenticate_user(username: str) -> UseBase:

#     query = users_database.select().filter_by(username=username)
#     user = await db.fetch_one(query)

#     if user:
#         return user
#     return False


# async def verify_email(email: str):

#     query = users_database.select().filter_by(email=email)

#     result = await db.fetch_one(query)

#     if result:
#         return True


# async def get_active_user(username: str):

#     query = (
#         select(
#             [users_database.c.id,
#              users_database.c.username,
#              users_database.c.enabled,
#              user_roles.c.role.label("role")])
#         .filter(
#             users_database.c.username == username
#         )
#         .join(user_roles, users_database.c.role_id == user_roles.c.id)

#     )
#     user = await db.fetch_one(query)

#     if user:
#         return _serialize_active_user(user)
#     return False


# async def create_user_db(user: User):

#     query = users_database.insert()

#     result = await db.execute(query, values=user.dict())

#     if result:
#         return _serialize_user({**user.dict(), "id": result})

#     return _serialize_user(result)


async def get_all_user():
    
    

    async with async_session() as session:
        query = await session.execute(select(Users))
        users = query.scalars().all()

        
        return _serialize_users(users)


async def select_user(user_id: int):

    async with async_session() as session:
        user = await session.get(Users, user_id)        

    if not user:
        return False

    return _serialize_user(user)


# async def update_user_db(user_id: int, user_data: User):
#     query = users_database.update().where(
#         users_database.c.id == user_id).returning(users_database.c.id)

#     user = await db.execute(query, values=user_data.dict())
#     if user:
#         return _serialize_user({**user_data.dict(), "id": user})

#     return False

#     return {"succes": True}


def _serialize_users(users: list):

    return list(map(lambda x: {
        "id": x.id,
        "username": x.username,
        "email": x.email,
        "enabled": x.enabled,
        
    }, users))


def _serialize_user(user):

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "enabled": user.enabled,
        
    }


# def _serialize_active_user(user: db):

#     return {
#         "id": user.get("id"),
#         "enabled": user.get("enabled"),
#         'role': user.get("role")
#     }
