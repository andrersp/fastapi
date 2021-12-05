# -*- coding: utf-8 -*-
from sqlalchemy import literal_column, select
from app.models.user import users_database, user_roles
from app.ext.database import db
from app.core.schemas.user import UserInDB, User


async def authenticate_user(username: str) -> UserInDB:

    query = users_database.select().filter_by(username=username)
    user = await db.fetch_one(query)

    if user:
        return user
    return False


async def verify_email(email: str):

    query = users_database.select().filter_by(email=email)

    result = await db.fetch_one(query)

    if result:
        return True


async def get_active_user(username: str):

    query = (
        select(
            [users_database.c.id,
             users_database.c.username,
             users_database.c.enabled,
             user_roles.c.role.label("role")])
        .filter(
            users_database.c.username == username
        )
        .join(user_roles, users_database.c.role_id == user_roles.c.id)

    )
    user = await db.fetch_one(query)

    if user:
        return _serialize_active_user(user)
    return False


async def create_user_db(user: UserInDB):

    query = users_database.insert()

    result = await db.execute(query, values=user.dict())

    if result:
        return _serialize_user({**user.dict(), "id": result})

    return _serialize_user(result)


async def get_all_user():

    query = (select(
        [users_database, user_roles.c.name.label("role_name")])
        .join(user_roles, users_database.c.role_id == user_roles.c.id))

    users = await db.fetch_all(query)

    return _serialize_users(users)


async def select_user(user_id: int):

    query = (select(users_database, user_roles.c.name.label("role_name"))
             .filter(users_database.c.id == user_id)
             .join(user_roles, users_database.c.role_id == user_roles.c.id)

             )

    user = await db.fetch_one(query)

    if not user:
        return False

    return _serialize_user(user)


async def update_user_db(user_id: int, user_data: User):
    query = users_database.update().where(
        users_database.c.id == user_id).returning(users_database.c.id)

    user = await db.execute(query, values=user_data.dict())
    if user:
        return _serialize_user({**user_data.dict(), "id": user})

    return False

    return {"succes": True}


def _serialize_users(users: list):

    return list(map(lambda x: {
        "id": x.get('id'),
        "username": x.get('username'),
        "email": x.get('email'),
        "enabled": x.get('enabled'),
        "access_role": {"role_id": x.get("role_id"), "role_name": x.get("role_name")}
    }, users))


def _serialize_user(user: db):

    return {
        "id": user.get("id"),
        "username": user.get("username"),
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "enabled": user.get("enabled"),
        "access_role": {"role_id": user.get("role_id"), "role_name": user.get("role_name")}
    }


def _serialize_active_user(user: db):

    return {
        "id": user.get("id"),
        "enabled": user.get("enabled"),
        'role': user.get("role")
    }
