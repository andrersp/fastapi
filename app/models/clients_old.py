# -*- coding: utf-8 -*-

from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from typing import List


from sqlalchemy import String, Column, Integer, Table, ForeignKey
from sqlalchemy.orm import registry, relationship

from app.ext.database import metadata


mapper_registry = registry(metadata)

@dataclass()
class ClientAddress:
    id: int = field(init=False)
    street = str = None
    client_id: int = field(init=False)

@dataclass()
class Client:
    id: int = field(init=False)
    name: str = None
    email: str = None
    phone: str = None
    address: List[ClientAddress] = field(default_factory=list)



client_databse = Table(
    'client',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(40), index=True),
    Column('email', String(40), index=True),
    Column('phone', String(10))
)


client_address_database = Table(
    'client_address',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('street', String()),
    Column('client_id', ForeignKey(client_databse.c.id), nullable=False)
)

mapper_registry.map_imperatively(Client, client_databse, properties={
    'addresses': relationship(ClientAddress, backref='client', order_by=client_address_database.c.id),
})

mapper_registry.map_imperatively(ClientAddress, client_address_database)