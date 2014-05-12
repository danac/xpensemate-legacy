#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..db import DBInterface
from .expense_balance import Balance
import itertools

class ExpenseManager:

    def __init__(self, db_file=""):
        self.db_file = db_file
        self.db_interface = DBInterface(db_file)
        self.cached_balances = None
        self.cached_global_balance = None
        self.cached_balances_map = dict()

    def clear_cache(self):
        self.cached_balances = None
        self.cached_global_balance = None
        self.cached_balances_map = dict()
      
    def get_open_balances(self):
        if self.cached_balances is not None and self.cached_global_balance is not None:
            return self.cached_balances, self.cached_global_balance
            
        balances = self.db_interface.get_open_balances()
        debtors = set()
        for balance in balances:
            names = [person.name for person in balance.persons]
            for name in names:
                debtors.add(name)
        debtor_pairs = itertools.combinations(debtors, 2)

        # Now compute the overall debts
        global_balance = Balance()
        global_balance.debtors = debtors
        global_balance._reset()

        # Gather the debts
        for balance in balances:
            balance.calculate()
            for debtor, debts in balance.personal_debts.items():
                for receiver, amount in debts.items():
                    if not receiver in global_balance.personal_debts[debtor].keys():
                        global_balance.personal_debts[debtor][receiver] = 0
                    global_balance.personal_debts[debtor][receiver] += amount

        # Get rid of "bidirectional debts"
        for pair in debtor_pairs:
            p1, p2 = pair
            try:
                debt1 = global_balance.personal_debts[p1][p2]
                debt2 = global_balance.personal_debts[p2][p1]
                global_balance.personal_debts[p1][p2] -= min(debt1, debt2)
                global_balance.personal_debts[p2][p1] -= min(debt1, debt2)
            except KeyError:
                pass
                
        # Get rid of null debts
        for debtor in global_balance.personal_debts.keys():
          global_balance.personal_debts[debtor] = \
              {key: value for key, value in global_balance.personal_debts[debtor].items() if value != 0.0}
        global_balance.personal_debts = \
              {key: value for key, value in global_balance.personal_debts.items() if len(value) > 0}

        # Simplify debts
        debtors = global_balance.personal_debts.keys()
        for p1 in sorted(debtors):
            receivers = global_balance.personal_debts[p1].keys()
            for p2 in sorted(list(set(debtors) & set(receivers))):
              other_receivers = global_balance.personal_debts[p2].keys()
              common_receivers = set(receivers) & set(other_receivers)
              print("Common receivers: {} between {} and {}".format(common_receivers, p1, p2))
              for receiver in sorted(list(common_receivers)):
                  print("Looking at {}...".format(receiver))
                  if global_balance.personal_debts[p2][receiver] == 0.0 or \
                      global_balance.personal_debts[p1][receiver] == 0.0:
                          print("continue (0.0 for {} in {} or {}".format(receiver, p1, p2))
                  else:
                      print("Looking at debts for {} between {} and {}".format(receiver, p1, p2))
                      amount = min(global_balance.personal_debts[p1][p2], global_balance.personal_debts[p2][receiver])
                      global_balance.personal_debts[p2][receiver] -= amount
                      global_balance.personal_debts[p1][p2] -= amount
                      global_balance.personal_debts[p1][receiver] += amount
                      print("Simplified {} for {} from {} to {}".format(amount, receiver, p2, p1))               

        # Get rid of null debts
        for debtor in global_balance.personal_debts.keys():
          global_balance.personal_debts[debtor] = \
              {key: value for key, value in global_balance.personal_debts[debtor].items() if value != 0.0}
        global_balance.personal_debts = \
              {key: value for key, value in global_balance.personal_debts.items() if len(value) > 0}

        self.cached_balances = balances
        self.cached_global_balance = global_balance
        
        return balances, global_balance

    def get_closed_balances(self):
        balances = self.db_interface.get_closed_balances()
        return balances

    def get_balance(self, bal_id):
        if bal_id in self.cached_balances_map.keys():
            return self.cached_balances_map[bal_id]
        
        balance = self.db_interface.get_balance(id=bal_id)
        balance.calculate()
        self.cached_balances_map[bal_id] = balance
        return balance

    def close_balance(self, id):
        self.clear_cache()
        self.db_interface.close_balance(balance_id=id)

    def add_balance(self, debtors):
        self.clear_cache()
        debtors_parse = debtors.split(',')
        debtors_list = []
        for name in debtors_parse:
            if name != "":
                debtors_list.append(name.strip().title())
        self.db_interface.add_balance(debtors_list)

    def get_persons(self):
        return self.db_interface.get_persons()

    def add_expense(self, year, month, day, buyer, amount, description, balance_id):
        self.clear_cache()
        name = buyer.strip().title()
        desc = description.strip()
        y = int(year)
        m = int(month)
        d = int(day)
        money = float(str(amount).upper().replace('CHF', '').strip())
        self.db_interface.add_expense(year=y,
                                      month=m,
                                      day=d,
                                      buyer=name,
                                      description=desc,
                                      amount=money,
                                      balance_id=balance_id)

    def delete_expense(self, expense_id):
        self.clear_cache()
        i = int(expense_id)
        self.db_interface.delete_expense(i)

    def __repr__(self):
        string = ""
        string += "OPEN BALANCES\n"
        open_bal = self.get_open_balances()
        if len(open_bal) > 0:
            for bal in self.get_open_balances():
                string += str(bal)
        string += "CLOSED BALANCES\n"
        closed_bal = self.get_closed_balances()
        if len(closed_bal) > 0:
            for cbal in self.get_closed_balances():
                string += str(cbal)
        string += '\n'
        return string
