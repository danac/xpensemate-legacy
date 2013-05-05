#!/usr/bin/python
# -*- coding: utf-8 -*-

from .db import DBInterface

class ExpenseManager:

    def __init__(self, db_file = ""):
        self.db_file = db_file
        self.db_interface = DBInterface(db_file)

    def get_open_balances(self):
        balances = self.db_interface.get_open_balances()
        return balances

    def get_balance(self, id):
        balance = self.db_interface.get_balance(id = id)
        return balance
