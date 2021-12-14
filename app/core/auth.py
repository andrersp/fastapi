# -*- coding: utf-8 -*-

from sqlalchemy import event, text

from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.ext.settings import settings
from app.ext.exceptions import CustomException

from app.crud import users as crud_user
from app.ext.database import async_session
from app.models.user import Users, TokenStr, UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login", auto_error=False)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_passowod, hashed_password):
    return pwd_context.verify(plain_passowod, hashed_password)


def get_password_hashed(plain_passowod):
    return pwd_context.hash(plain_passowod)


async def authenticate_user(username, password):

    user = await crud_user.authenticate_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=int(settings.ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def get_user(username: str):
    user = await crud_user.get_active_user(username)
    if user:
        return user


async def verify_email(email: str):

    user = await crud_user.verify_email(email)

    if user:
        return user


async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = CustomException(status_code=401,
                                            message='Could not valide credential')

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])

        username = payload.get("sub")

        if not username:
            raise credentials_exception

        token_data = TokenStr(username=username)
    except JWTError as e:

        raise credentials_exception

    user = await get_user(username=token_data.username)

    if not user:
        raise credentials_exception

    if not user.enabled:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail='Inactive User')
    return user


@event.listens_for(UserRole.__table__, "after_create")
def create_fist_user(target, connection = async_session().connection(), **kwargs):

    roles = [
        {
            "name": "Administrator",
            "role": "role:admin"
        },
        {
            "name": "Developer",
            "role": "role:dev"
        }
        ]
    
    for role in roles:
        connection.execute(text(
            'INSERT INTO "roles" (name, role) '
            f"VALUES ('{role.get('name')}', '{role.get('role')}')") )

@event.listens_for(Users.__table__, "after_create")
def create_fist_user(target, connection = async_session().connection(), **kwargs):

    password = get_password_hashed('admin')
    connection.execute(text(
        'INSERT INTO "user" (username, password, full_name, email,  enabled, role_id) '
        f"VALUES ('admin', '{password}', 'andre luis', 'email@mail.com', True, 2)") )