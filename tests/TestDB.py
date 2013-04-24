#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from expense_manager.db import DBInterface
import hashlib, os, tempfile, inspect

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
        interface_memory.createStructure()

    def test_structure_to_file(self):
        fname = os.path.join(tempfile.gettempdir(), "__expense_manager_test_db.db")
        interface_to_file = DBInterface(fname)
        interface_to_file.createStructure()
        fhdl = open(fname, 'rb')
        digest = hashlib.md5(fhdl.read()).hexdigest()
        fhdl.close()
        #os.remove(fname)
        assert digest == "d460c690bfffc07a7b49691f2bc3e2e6"

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
        persons = self.iface.getPersons()
        assert persons.__repr__() == "['Dana', 'Alizée', 'Loïc', 'Mick']"

    def test_query_open_balance(self):
        balances = self.iface.getOpenBalances()
        assert balances.__repr__() == "[Balance 1, shared by Dana, Mick, 1 expense(s).]"

    def test_query_closed_balance(self):
        balances = self.iface.getClosedBalances()
        assert balances.__repr__() == "[Balance 2, shared by Dana, Alizée, Loïc closed on 2013-04-16, 1 expense(s).]"

    def test_query_expense(self):
        expense = self.iface.getExpense(year=2013, day=29, id=2)
        assert expense.__repr__() == "[Expense 2, 0.5 by Dana on 2013-04-29.]"

