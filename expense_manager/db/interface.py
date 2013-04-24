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
        self.session = self.Session()
        Log.info("Record database opened")

    def createStructure(self):
        model.createStructure(self.engine)

    def getOpenBalances(self):
        open_balances = []

        query = (
            self.session.query(model.DbBalance)
                .filter(model.DbBalance.year == None)
                .order_by(model.DbBalance.id) )

        for balance in query:
            open_balances.append(balance.makeBalance())

        return open_balances

    def getClosedBalances(self):
        closed_balances = []

        query = ( self.session.query(model.DbBalance)
            .filter(model.DbBalance.year != None)
            .order_by(model.DbBalance.id) )

        for balance in query:
            closed_balances.append(balance.makeBalance())

        return closed_balances

    def getPersons(self):
        return [row[0] for row in self.session.query(model.DbPerson).values(model.DbPerson.name)]

    def getExpense(self, **kwargs):
        query = self.session.query(model.DbExpense)
        for key in kwargs:
            query = query.filter(getattr(model.DbExpense, key) == kwargs[key])
        return [db_exp.makeExpense() for db_exp in query]
