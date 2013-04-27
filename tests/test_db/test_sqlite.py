#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from expense_manager.db import DBInterface
import hashlib, os, tempfile, inspect
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
        assert persons.__repr__() == "['Dana', 'Alizée', 'Loïc', 'Mick']"

    def test_query_open_balances(self):
        balances = self.iface.get_open_balances()
        assert balances.__repr__() == "[Balance 1, shared by Dana, Mick, 1 expense(s).]"

    def test_query_closed_balances(self):
        balances = self.iface.get_closed_balances()
        assert balances.__repr__() == "[Balance 2, shared by Dana, Alizée, Loïc closed on 2013-04-16, 1 expense(s).]"

    def test_query_expense(self):
        expense = self.iface.get_expenses(year=2013, day=29, id=2)
        assert expense.__repr__() == "[Expense 2, 0.5 by Dana on 2013-04-29.]"

