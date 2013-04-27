#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..core import Log
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

    def create_structure(self):
        model.create_structure(self.engine)

    def get_open_balances(self):
        open_balances = []

        query = (
            self.session.query(model.DbBalance)
                .filter(model.DbBalance.year == None)
                .order_by(model.DbBalance.id) )

        for balance in query:
            open_balances.append(balance.make_balance())

        return open_balances

    def get_closed_balances(self):
        closed_balances = []

        query = ( self.session.query(model.DbBalance)
            .filter(model.DbBalance.year != None)
            .order_by(model.DbBalance.id) )

        for balance in query:
            closed_balances.append(balance.make_balance())

        return closed_balances

    def get_persons(self):
        return [row[0] for row in self.session.query(model.DbPerson).values(model.DbPerson.name)]

    def get_expenses(self, **kwargs):
        query = self.session.query(model.DbExpense)
        for key in kwargs:
            query = query.filter(getattr(model.DbExpense, key) == kwargs[key])
        return [db_exp.make_expense() for db_exp in query]
