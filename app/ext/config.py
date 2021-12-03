# -*- coding: utf-8 -*-
from importlib import import_module
from app.ext.settings import settings


def init_app(app):
    for extension in settings.EXTENSIONS:
        mod = import_module(extension)
        mod.init_app(app)
