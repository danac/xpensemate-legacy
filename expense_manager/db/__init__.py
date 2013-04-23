#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.engine import Engine

@sqlalchemy.event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

from .interface import DBInterface
