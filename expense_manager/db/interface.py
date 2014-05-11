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
        self.create_structure()
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

    def add_balance(self, names):
        db_balance = model.DbBalance.create(names, self.session)
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

    def add_expense(self,
                    year,
                    month,
                    day,
                    buyer,
                    description,
                    amount,
                    balance_id):
        balance = self._query_balance_by_id(balance_id)
        balance_id = balance.id
        db_expense = model.DbExpense.create(year=year,
                                            month=month,
                                            day=day,
                                            buyer=buyer,
                                            description=description,
                                            amount=amount,
                                            balance_id=balance_id,
                                            session=self.session)
        balance.expenses.append(db_expense)
        try:
            balance.sanity_check()
            self.session.add(db_expense)
            self.session.commit()
        except:
            balance.expenses.pop()
            self.session.rollback()
            raise
            
    def delete_expense(self, expense_id):
        expense = self._query_expense_by_id(expense_id)
        self.session.delete(expense)
        self.session.commit()

    def get_open_balances(self):
        query = (
            self.session.query(model.DbBalance)
                .filter(model.DbBalance.year == None)
                .order_by(model.DbBalance.id) )
        return query

    def get_global_balance(self):
        query = (
            self.session.query(model.DbBalance)
                .filter(model.DbBalance.year == None)
                .order_by(model.DbBalance.id) )
        debtors = set()
        for balance in query:
            names = [person.name for person in balance.persons]
            for name in names:
                debtors.add(name)
        global_balance = model.DbBalance.create(debtors, self.session)
        return global_balance

    def get_closed_balances(self):
        query = ( self.session.query(model.DbBalance)
            .filter(model.DbBalance.year != None)
            .order_by(model.DbBalance.id) )
        return query

    def get_persons(self):
        query = self.session.query(model.DbPerson).values(model.DbPerson.name)
        return [row[0] for row in query]

    def get_expenses(self, **kwargs):
        query = self.session.query(model.DbExpense)
        for key in kwargs:
            # Special treatment in case of a buyer filter (relationship)
            if key == "buyer":
                query = query.filter(model.DbPerson.name == kwargs[key])
                continue
            query = query.filter(getattr(model.DbExpense, key) == kwargs[key])
        return query

    def get_balance(self, id):
        return self._query_balance_by_id(id)
