#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..core import Expense, Balance, Log
from . import model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBInterface:

    def __init__(self, database= "", echo = False):
        db_path = ""
        if database == "":
            db_path = "sqlite://"
        else:
            db_path = "sqlite:///" + database
        self.engine = create_engine(db_path, echo=echo)
        self.Session = sessionmaker(bind=self.engine)
        Log.info("Record database opened")

    def createStructure(self):
        model.createStructure(self.engine)

    def getOpenBalances(self):
        session = self.Session()
        open_balances = []
        for balance in ( session.query(model.DbBalance)
                            .filter(model.DbBalance.year == None)
                            .order_by(model.DbBalance.id) ):
            open_balances.append(balance.makeBalance())
        return open_balances
