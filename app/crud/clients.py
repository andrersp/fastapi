# -*- coding: utf-8 -*-

from app.ext.database import db
from app.models.clients import client_databse
from app.core.schemas.clients import Client


async def get_all_client():

    query = client_databse.select()

    clients = await db.fetch_all(query)

    return clients


async def insert_client(client: Client):

    query = client_databse.insert()

    result = await db.execute(query, values=client.dict())

    if result:
        return True
