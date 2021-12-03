# -*- coding: utf-8 -*-

from app.models.user import ModelUser
from app.ext.database import Session, get_session
from app.core.schemas.user import UserInDB


def create_user_db(user: UserInDB):

    with get_session() as session:
        # primary_key(user.dict())

        user = ModelUser(**user.dict())
        session.add(user)
        session.commit()
        session.refresh(user)

        return _serialize_user(user)


def get_all_user():
    with get_session() as session:
        users = session.query(ModelUser).order_by(
            ModelUser.username.desc()).all()
    return _serialize_users(users)


def select_user(user_id: int):

    with get_session() as session:
        user = session.query(ModelUser).get(user_id)

    if not user:
        return False
    return _serialize_user(user)


def updat_user_db(user_id: int, username: str, email: str, enabled: bool, full_name: str):

    with get_session() as session:
        user = session.query(ModelUser).get(user_id)
        user.username = username
        user.email = email
        user.enabled = enabled
        user.full_name = full_name
        session.add(user)
        session.commit()
        session.refresh(user)

    if not user:
        return False
    return _serialize_user(user)


def _serialize_users(users: list):

    return list(map(lambda x: {
        "id": x.id,
        "username": x.username,
        "email": x.email,
        "enabled": x.enabled
    }, users))


def _serialize_user(user: ModelUser):

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "enabled": user.enabled
    }
