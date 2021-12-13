# -*- coding: utf-8 -*-

from fastapi import APIRouter
from typing import List

from app.core.http_responses import success, error
# from app.crud import clients as crud_client
from app.core.schemas.clients import Client, ClientInDB
from app.core.access_role import acl_roles, Permission


router = APIRouter(tags=['Clients'])


@router.get("/client", response_model=List[ClientInDB])
async def get_clients(page: int = 0, limit: int = 5,  ):

    clients = await crud_client.get_all_client(page, limit)

    return clients


@router.post("/client")
async def insert_client(client: Client):

    cad = await crud_client.insert_client(client)

    return success(status_code=201)


@router.get('/client/{client_id}')
async def select_client(client_id: int):

    client = await crud_client.select_client(client_id)

    return success()
