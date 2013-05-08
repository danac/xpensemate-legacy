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

    def add_expense(self, year, month, day, buyer, amount, description, balance_id):
        name = buyer.strip().title()
        desc = description.strip()
        y = int(year)
        m = int(month)
        d = int(day)
        money = float(str(amount).upper().replace('CHF', '').strip())
        expense = Expense(year=y, month=m, day=d, buyer=name, description=desc, amount=money)
        balance = self.db_interface.get_balance(id=int(balance_id))
        balance.add_expense(expense)
        self.db_interface.add_expense(expense, balance_id)

    def delete_expense(self, expense_id):
        i = int(expense_id)
        self.db_interface.delete_expense(i)

    def __repr__(self):
        s = ""
        s += "OPEN BALANCES\n"
        open = self.get_open_balances()
        if len(open) > 0:
            for bal in self.get_open_balances():
                s += str(bal)
        s += "CLOSED BALANCES\n"
        closed = self.get_closed_balances()
        if len(closed) > 0:
            for cbal in self.get_closed_balances():
                s += str(cbal)
        s += '\n'
        return s
