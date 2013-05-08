#!/usr/bin/python

from expense_manager import ExpenseManager, Balance, Expense
import sqlite3 as lite

db_fname = "expenses.db"
old_db_fname = "torestore.db"
exp_mgr = ExpenseManager(db_fname)
exp_mgr.db_interface.create_structure()

colocs = "Dana, Mick, Alizée, Loïc"
exp_mgr.add_balance(colocs)
balID = exp_mgr.get_open_balances()[0].ID

handle = lite.connect(old_db_fname)
handle.text_factory = str
handle.row_factory = lite.Row
cursor = handle.cursor()

sql = "SELECT * FROM expenses ORDER BY id"

query = cursor.execute(sql)
for row in query:
    exp_mgr.add_expense(year = int(row['year']), month = int(row['month']), day = int(row['day']), amount = float(row['amount']), buyer = row['name'], description = row['description'], balance_id = balID)
    print("Added: " + str(dict(row)))

print(exp_mgr)
