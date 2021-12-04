# -*- coding: utf-8 -*-

from fastapi import FastAPI

from databases import Database
from sqlalchemy import create_engine, MetaData

from app.ext.settings import settings


db = Database(settings.DATABASE_URL)

metadata = MetaData()

engine = create_engine(settings.DATABASE_URL, connect_args={})


async def startup():
    await db.connect()


async def shutdown():
    await db.disconnect()


def init_app(app: FastAPI):
    metadata.create_all(engine)
    app.add_event_handler('startup', startup)
    app.add_event_handler('shutdown', shutdown)
