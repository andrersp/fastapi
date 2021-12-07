# -*- coding: utf-8 -*-

from fastapi import APIRouter
from typing import List

from app.core.http_responses import success, error
from app.crud import clients as crud_client
from app.core.schemas.clients import Client
from app.core.access_role import acl_roles, Permission


router = APIRouter(tags=['Clients'])


@router.get("/client", response_model=List[Client])
async def get_clients(acls: list = Permission('operator', acl_roles)):

    clients = await crud_client.get_all_client()

    return clients


@router.post("/client")
async def insert_client(client: Client, acls: list = Permission('admin', acl_roles)):

    cad = await crud_client.insert_client(client)

    return success()
