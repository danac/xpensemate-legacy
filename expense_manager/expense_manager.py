#!/usr/bin/python
# -*- coding: utf-8 -*-

from .db import DBInterface
from .core import Balance, Expense

class ExpenseManager:

    def __init__(self, db_file = ""):
        self.db_file = db_file
        self.db_interface = DBInterface(db_file)

    def get_open_balances(self):
        balances = self.db_interface.get_open_balances()
        return balances

    def get_closed_balances(self):
        balances = self.db_interface.get_closed_balances()
        return balances

    def get_balance(self, id):
        balance = self.db_interface.get_balance(id = id)
        return balance

    def close_balance(self, id):
        self.db_interface.close_balance(balance_id = id)

    def add_balance(self, debtors):
        debtors_parse = debtors.split(',')
        debtors_list = []
        for name in debtors_parse:
            if name != "":
                debtors_list.append(name.strip().title())
        balance = Balance(debtors_list)
        self.db_interface.add_balance(balance)

    def get_persons(self):
        return self.db_interface.get_persons()
