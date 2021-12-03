# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import ModelUser
from app.core.schemas.user import Token, UserResponse, UserInDB, User
from app.crud.users import create_user_db, get_all_user, select_user, updat_user_db
from app.core import auth
from app.core.http_responses import error, success


router = APIRouter(tags=['Login'])


@router.post("/login", response_model=Token)
async def login_for_access_user(form_data: OAuth2PasswordRequestForm = Depends()):

    user = auth.authenticate_user(form_data.username, form_data.password)

    if not user:
        return error({"msg": "Incorrect User Name or Passowrd"}, 401)

    if not user.enabled:
        return error({"msg": "Inactive User"}, 400)

    access_token = auth.create_access_token(
        data={'sub': user.username, "id": user.id, "email": user.email})

    data = {"access_token": access_token, 'token_type': 'bearer',
            "email": user.email, "username": user.username}

    return success(data)
