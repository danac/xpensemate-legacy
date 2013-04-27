#!/usr/bin/python

from .expense import ExpenseManager, Expense, Balance
from .db import DBInterface
from .common import Log
import logging, sys

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    exp = Expense(2, 2013, 4, 20, "Dana", 10.50, "Trucs...")
    print(exp)
    e = Balance(1, ["Dana"], 2013, 2, 10)
    print(e)
    e.calculate()
    try:
        pass
        #e.sanityCheck()
    except AssertionError as bug:
        print("Erreur d'assertion:", bug)

    e.addExpense(exp)
    print(e)

    print("TESTING DB")
    interface = DBInterface("expenses2.db")

    for balance in interface.get_open_balances():
        print(balance)
        print("-----")
