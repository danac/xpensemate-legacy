#!/usr/bin/python
# -*- coding: utf-8 -*-

from .expense import Expense, Balance

class DBInterface:

    db_file = ""
    echo_flag = False

    db_model = None
    Session = None
    db_file = ""

    @classmethod
    def init_db(cls, database):
        cls.db_file = database
        from . import db_model
        print(db_model.__dict__)
        cls.db_model = db_model.model
        cls.Session = db_model.Session

    @classmethod
    def getOpenBalances(cls):
        session = cls.Session()
        open_balances = []
        for balance in ( session.query(cls.db_model.DbBalance)
                            .filter(cls.db_model.DbBalance.year == None)
                            .order_by(cls.db_model.DbBalance.id) ):
            open_balances.append(balance.makeBalance())
        return open_balances
