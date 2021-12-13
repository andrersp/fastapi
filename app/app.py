# -*- coding: utf-8 -*-
from fastapi import FastAPI

from .ext import config

def minimal_app():
    app = FastAPI(docs_url="/v1/docs", redoc_url='/v1/redoc')

    return app


def create_app():
    app = minimal_app()
    config.init_app(app)
    return app
