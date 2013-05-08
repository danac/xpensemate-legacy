#!/usr/bin/python
from expense_manager import ExpenseManager
from expense_manager.web import app
import inspect
import os.path

prefix = ""
hostname = "donjon.terra-amata"
db_file = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "expenses.db")
exp_mgr = ExpenseManager(db_file)
webapp = app(exp_mgr, prefix, 'http://' + hostname)
webapp.run(host=hostname, port=8080)
