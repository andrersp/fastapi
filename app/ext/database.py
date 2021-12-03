# -*- coding: utf-8 -*-

from contextlib import contextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ as env

engine = create_engine(env.get('SQLALCHEMY_DATABASE_URI'),
                       connect_args={})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_app(app: FastAPI):
    Base.metadata.create_all(engine)


@contextmanager
def get_session():
    session = Session()

    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
