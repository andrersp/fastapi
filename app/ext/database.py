# -*- coding: utf-8 -*-

from fastapi import FastAPI
import os

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.ext.settings import settings



engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)    




async def get_session() -> AsyncSession:    
    
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

def init_app(app: FastAPI):    
    app.add_event_handler('startup', init_db)
    # app.add_event_handler('shutdown', shutdown)
