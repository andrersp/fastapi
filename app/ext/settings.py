import os
import pathlib
from functools import lru_cache


class BaseConfig:

    DATABASE_URL: str = os.environ.get("SQLALCHEMY_DATABASE_URI")
    DATABASE_CONNECT_DICT: dict = {}
    EXTENSIONS = ['app.routers.v1', "app.ext.database", 'app.ext.cors']
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_HOURS = os.environ.get("ACCESS_TOKEN_EXPIRE_HOURS")


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
