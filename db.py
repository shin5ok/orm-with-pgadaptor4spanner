#!/usr/bin/env python

from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker
import click
import os
import json
import logging
from datetime import datetime, timezone
import typing
from typing import *

DSN: str = os.environ.get("DSN", "postgresql://@localhost/game")
engine = create_engine(DSN)

debug_flag: bool = "DEBUG" in os.environ
logging.basicConfig()
loggingConfig = logging.getLogger('sqlalchemy.engine')
if debug_flag:
    loggingConfig.setLevel(logging.DEBUG)

Base = declarative_base()
class Users(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

users = Table('users', MetaData(bind=engine),
            Column('user_id', String(32), primary_key=True),
            Column('name', String(32)),
            Column('created_at', TIMESTAMP(timezone=False)),
            Column('updated_at', TIMESTAMP(timezone=False)),
        )

@click.group()
def cli() -> None:
    pass

@cli.command()
@click.option("--name", "-n")
def put(name: str) -> None:
    writing(name) 

def writing(name: str) -> None:
    import uuid

    try:
        with engine.begin() as connection:
            user_id = str(uuid.uuid4())
            dt = datetime.now(timezone.utc)
            r = {"user_id": user_id, "name": name, "created_at": dt, "updated_at":dt}
            connection.execute(users.insert(), r)
    except Exception as e:
        print(str(e))

@cli.command()
@click.option("--name", "-n")
def search(name: str) -> slice:
    try:
        session = sessionmaker(bind=engine)()
        result = session.query(Users).filter(Users.name==name)
        data = ([[v.name, v.user_id] for v in result])
        print(data)
        return data
    except Exception as e:
        print(str(e))
        return ()


if __name__ == '__main__':
    cli()
