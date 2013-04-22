#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..db import DBInterface as DBConfig
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

@sqlalchemy.event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

db_address = "sqlite:///" + DBConfig.db_file
echo_flag = DBConfig.echo_flag

engine = create_engine(db_address, echo=echo_flag)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

from . import model
