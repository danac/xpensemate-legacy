#!/usr/bin/python

from .core import Expense, Balance, Log
from .db import DBInterface
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

    e.add_expense(exp)
    print(e)
