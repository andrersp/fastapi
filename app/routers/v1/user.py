# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

# from app.models.user import ModelUser
from app.core.schemas.user import Token, UserResponse, UserInDB, User
from app.crud.users import create_user_db, get_all_user, select_user, update_user_db, verify_email
from app.core import auth
from app.core.http_responses import error, success


router = APIRouter(tags=['User'], dependencies=[
                   Depends(auth.get_current_user)])


@router.post('/user')
async def create_user(user: UserInDB):

    username = user.username
    email = user.email
    if await auth.get_user(username):
        return error(["User Exists!"])

    if await auth.verify_email(email):
        return error(["E-mail Existsts!"])

    user.password = auth.get_password_hashed(email)

    try:
        user = await create_user_db(user)
    except Exception as e:
        return error(["Internal error"], 500)
    else:
        return success(user,  status_code=201)

    return True


@ router.get("/user")
async def get_users():

    users = await get_all_user()
    return success({"data": users})


@ router.get("/user/{user_id}")
async def get_user(user_id: int):

    user = await select_user(user_id)

    if not user:
        return error(["user Not Found"], 404)

    return success(user)


@ router.put("/user/{user_id}")
async def update_user(user_id: int, user_data: User):

    try:
        user = await update_user_db(user_id, user_data)

    except Exception as e:
        return error(status_code=500)

    else:
        if not user:
            return error(['User not found!'], status_code=404)
        return success(user)
