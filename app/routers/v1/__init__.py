# -*- coding: utf-8 -*-

from fastapi import FastAPI

from app.routers.v1.user import router as user_router
from app.routers.v1.login import router as login_router
# from app.routers.v1.clients import router as client_router


def init_app(app: FastAPI):
    app.include_router(user_router, prefix="/v1")
    app.include_router(login_router, prefix="/v1")
    # app.include_router(client_router, prefix='/v1')
