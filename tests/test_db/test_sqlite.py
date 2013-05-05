#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from expense_manager.db import DBInterface
from expense_manager.core import Balance, Expense
import hashlib, os, tempfile, inspect, datetime
import sqlite3

class TestSQLiteIO:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_structure_to_memory(self):
        interface_memory = DBInterface("")
        interface_memory.create_structure()

    def test_structure_to_file(self):
        fname = os.path.join(tempfile.gettempdir(), "__expense_manager_test_db.db")
        interface_to_file = DBInterface(fname)
        interface_to_file.create_structure()

        dump = ""
        con = sqlite3.connect(fname)
        for line in con.iterdump():
            dump += '%s\n' % line
        con.close()
        os.remove(fname)

        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        ref_fname = os.path.join(current_dir, "test_database.sql")
        dump_reference = open(ref_fname, 'r').read()

        assert_equals(dump, dump_reference, "Database dump differs from reference")

class TestSQLiteQuery:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        db_file = os.path.join(current_dir, "test_database.db")
        self.iface = DBInterface(db_file)

    def tearDown(self):
        pass

    def test_query_persons(self):
        persons = self.iface.get_persons()
        assert_equals(persons.__repr__(), "['Dana', 'Alizée', 'Loïc', 'Mick']")

    def test_query_open_balances(self):
        balances = self.iface.get_open_balances()
        print(balances[0].debtors)
        assert_equals(balances[0].__repr__(show_id=True), "Balance shared by Dana, Mick, 1 expense(s), Id 1.")

    def test_query_closed_balances(self):
        balances = self.iface.get_closed_balances()
        print(balances[0].debtors)
        assert_equals(balances[0].__repr__(indent=0, show_id=True), "Balance shared by Dana, Alizée, Loïc, closed on 2013-04-16, 1 expense(s), Id 2.")

    def test_query_expense(self):
        expenses = self.iface.get_expenses(year=2013, day=29, id=2)
        assert_equals(expenses[0].__repr__(show_id=True), "Expense 0.5 by Dana on 2013-04-29, Id 2.")


class TestSQLiteBalance:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        self.interface = DBInterface("")
        self.interface.create_structure()

    def tearDown(self):
        pass

    def test_add_closed_balance(self):
        balance = Balance(debtors = ["Dana", "Alizée", "Mik"], year = 2013, month = 2, day = 10)
        self.interface.add_balance(balance)
        resulting_balances = self.interface.get_closed_balances()
        assert_equals(len(resulting_balances), 1)
        assert_equals(resulting_balances[0].__repr__(), balance.__repr__())

    def test_add_open_balance(self):
        balance = Balance(debtors = ["Dana", "Alizée", "Mik"])
        self.interface.add_balance(balance)
        resulting_balances = self.interface.get_open_balances()
        assert_equals(len(resulting_balances), 1)
        assert_equals(resulting_balances[0].__repr__(show_id=False), balance.__repr__(show_id=False))

    def test_close_balance(self):
        balance = Balance(debtors = ["Dana", "Alizée", "Mik"])

        today = datetime.date.today()
        balance_closed = Balance(debtors = ["Dana", "Alizée", "Mik"], year = today.year, month = today.month, day = today.day)

        self.interface.add_balance(balance)
        balance = self.interface.get_open_balances()[0]
        self.interface.close_balance(balance.ID)

        resulting_balances = self.interface.get_open_balances()
        assert_equals(len(resulting_balances), 0)

        resulting_balances = self.interface.get_closed_balances()
        assert_equals(len(resulting_balances), 1)
        assert_equals(resulting_balances[0].__repr__(), balance_closed.__repr__())


class TestSQLiteExpense:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        self.interface = DBInterface("")
        self.interface.create_structure()
        balance = Balance(debtors = ["Dana", "Alizée", "Mik"])
        self.interface.add_balance(balance)
        open_bal = self.interface.get_open_balances()
        self.balance_id = open_bal[0].ID
        print(self.balance_id)

    def tearDown(self):
        pass

    def test_add_remove_expense(self):
        # Create an expense
        expense = Expense(year = 2013, month = 4, day = 20, buyer = "Dana", amount = 10.50, description = "Trucs...")
        # Add it to the open balance created in the setUp
        self.interface.add_expense(expense, self.balance_id)
        # Query the open balances
        resulting_balances = self.interface.get_open_balances()
        # There must be only one balance
        assert_equals(len(resulting_balances), 1)
        # There must be only one expense inside
        assert_equals(len(resulting_balances[0].expenses), 1)
        # It must be the one just inserted
        assert_equals(resulting_balances[0].expenses[0].__repr__(), expense.__repr__())
        # Query the expense
        expenses = self.interface.get_expenses(buyer = "Dana")
        # There must be only one
        assert_equals(len(expenses), 1)
        # It must still be the same
        assert_equals(expenses[0].__repr__(), expense.__repr__())
        # Get the Id
        expense_id = expenses[0].ID
        # Delete it
        self.interface.delete_expense(expense_id)
        # There must be no more expenses from that buyer
        expenses = self.interface.get_expenses(buyer = "Dana")
        assert_equals(len(expenses), 0)
        # It this must be thae case through the balance as well
        resulting_balances = self.interface.get_open_balances()
        assert_equals(len(resulting_balances), 1)
        assert_equals(len(resulting_balances[0].expenses), 0)


