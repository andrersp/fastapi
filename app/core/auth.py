# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy import or_, event

from app.ext.database import Session
from app.models.user import ModelUser
from app.ext.settings import settings
from app.core.schemas.user import User, UserInDB, TokenData
from app.core.exceptions import CustomException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login", auto_error=False)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_passowod, hashed_password):
    return pwd_context.verify(plain_passowod, hashed_password)


def get_password_hashed(plain_passowod):
    return pwd_context.hash(plain_passowod)


def authenticate_user(username, password):

    session = Session()
    user = session.query(ModelUser).filter_by(username=username).first()
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


def get_user(username: str, db: ModelUser = ModelUser):
    session = Session()
    user = session.query(db).filter_by(username=username).first()
    if user:
        return user


def verify_email(email: str, db: ModelUser = ModelUser):
    session = Session()
    user = session.query(db).filter(db.email == email).first()
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

        token_data = TokenData(username=username)
    except JWTError as e:

        raise credentials_exception

    # user = get_user(username=token_data.username)

    # if not user:
    #     raise credentials_exception

    # if not user.enabled:
    #     raise HTTPException(status.HTTP_400_BAD_REQUEST,
    #                         detail='Inactive User')
    return payload


# Create Fisrt User
@event.listens_for(ModelUser.__table__, 'after_create')
def create_fist_user(target, connection, **kwargs):
    password = get_password_hashed('admin')
    connection.execute(
        "INSERT INTO users (username, email, password, enabled) "
        f"VALUES ('admin', 'email@mail.com', '{password}', True)"

    )
