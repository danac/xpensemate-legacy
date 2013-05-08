#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..core import Log
from . import model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

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

    def _query_balance_by_id(self, balance_id):
        query = (
        self.session.query(model.DbBalance)
            .filter(model.DbBalance.id == balance_id) )
        assert query.count() == 1, "Several balances with same ID detected"
        return query.first()

    def _query_expense_by_id(self, expense_id):
        query = (
        self.session.query(model.DbExpense)
            .filter(model.DbExpense.id == expense_id) )
        assert query.count() == 1, "Several expenses with same ID detected"
        return query.first()

    def create_structure(self):
        model.create_structure(self.engine)

    def add_balance(self, balance):
        balance.sanity_check()
        db_balance = model.DbBalance()
        db_balance.from_balance(self.session, balance)

        self.session.merge(db_balance)
        self.session.commit()

    def close_balance(self, balance_id):
        balance = self._query_balance_by_id(balance_id)
        today = datetime.date.today()
        balance.year = today.year
        balance.month = today.month
        balance.day = today.day
        self.session.add(balance)
        self.session.commit()

    def add_expense(self, expense, balance_id):
        db_balance = self._query_balance_by_id(balance_id)
        Log.info(db_balance.make_balance())
        Log.info(expense)
        Log.info(self.get_persons())
        expense.sanity_check()
        db_expense = model.DbExpense()
        db_expense.from_expense(self.session, expense, db_balance)
        self.session.add(db_expense)
        self.session.commit()
        Log.info(self.get_persons())

    def delete_expense(self, expense_id):
        expense = self._query_expense_by_id(expense_id)
        self.session.delete(expense)
        self.session.commit()

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
            # Special treatment in case of a buyer filter (relationship)
            if key == "buyer":
                query = query.filter(model.DbPerson.name == kwargs[key])
                continue
            query = query.filter(getattr(model.DbExpense, key) == kwargs[key])
        return [db_exp.make_expense() for db_exp in query]

    def get_balance(self, id):
        return self._query_balance_by_id(id).make_balance()
