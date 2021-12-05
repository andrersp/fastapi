# -*- coding: utf-8 -*-
from sqlalchemy import literal_column
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


async def get_user_by_username(username: str):

    query = (users_database
             .join(user_roles)
             .select()
             .filter(users_database.c.username == username)

             )
    user = await db.fetch_one(query)

    if user:
        return _serialize_user(user)
    return False


async def create_user_db(user: UserInDB):

    query = users_database.insert()

    result = await db.execute(query, values=user.dict())

    if result:
        return _serialize_user({**user.dict(), "id": result})

    return _serialize_user(result)


async def get_all_user():

    query = users_database.select()

    users = await db.fetch_all(query)

    return _serialize_users(users)


async def select_user(user_id: int):

    query = (users_database
             .join(user_roles)
             .select()
             .filter(users_database.c.id == user_id)

             )

    user = await db.fetch_one(query)
    # if user:
    #     for key, value in user.items():
    #         print(f'{key}: {value}')

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

    # with get_session() as session:
    #     user = session.query(ModelUser).get(user_id)
    #     user.username = username
    #     user.email = email
    #     user.enabled = enabled
    #     user.full_name = full_name
    #     session.add(user)
    #     session.commit()
    #     session.refresh(user)

    # if not user:
    #     return False
    return {"succes": True}


def _serialize_users(users: list):

    return list(map(lambda x: {
        "id": x.get('id'),
        "username": x.get('username'),
        "email": x.get('email'),
        "enabled": x.get('enabled')
    }, users))


def _serialize_user(user: db):

    return {
        "id": user.get("id"),
        "username": user.get("username"),
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "enabled": user.get("enabled"),
        'role': user.get("role")
    }
