# -*- coding: utf-8 -*-
from typing import List
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from app.models.user import Users, UseBase, UserRole, UserUpdate
from app.ext.database import async_session, get_session


async def authenticate_user(username: str) -> UseBase:

    async with async_session() as session:
        query = select(Users).filter_by(username=username)
        user = await session.execute(query)
        result = user.scalar()
        
        

    if result:
        return result
    return False


async def verify_email(email: str):

    async with async_session() as session:
        query = select(Users).filter_by(email=email)
        user = await session.execute(query)
        result = user.scalar()      
        

    if result:
        return result
    return False


async def get_active_user(username: str):

    async with async_session() as session:
        query = select(Users).filter_by(username=username).options(selectinload(Users.role))
        user = await session.execute(query)
        result = user.scalar()
    if result:
        return result
    return False


async def create_user_db(user: Users):

    async with async_session() as session:
        user = Users(**user.dict())
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return  user




async def get_all_user():   

    async with async_session() as session:

        query = await session.execute(select(Users).options(selectinload(Users.role)))
        users = query.scalars() 

        
        return _serialize_users(users)


async def select_user(user_id: int):

    async with async_session() as session:
        query = select(Users).filter_by(id=user_id).options(selectinload(Users.role))
        query = await session.execute(query)
        user = query.scalar()

    if not user:
        return False

    return _serialize_user(user)


async def update_user_db(user_id: int, user_data: UserUpdate):
    
    async with async_session() as session:
        user = await session.get(Users, user_id)
        if not user:
            return False
        user.full_name = user_data.full_name
        user.email = user_data.email
        user.role_id = user_data.role_id
        user.enabled = user_data.enabled
        session.add(user)

        await session.commit()
        await session.refresh(user)
        return user
        
        
        
        

        
        


def _serialize_users(users: List[Users]):

    return list(map(lambda x: {
        "id": x.id,
        "username": x.username,
        "full_name": x.full_name,
        "email": x.email,
        "enabled": x.enabled,
        "role": x.role.name
    
        
    }, users))


def _serialize_user(user):

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role.name
    }



