#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from expense_manager.db import DBInterface
import hashlib, os, tempfile, inspect

class TestDBSQLite:

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
        assert digest == "bc6c6e6f3dc1e1106abd8b0946d1d682"

    def test_add_query_expense(self):
        pass

    def test_query_open_balance(self):
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        db_file = os.path.join(current_dir, "test_database.db")

        iface = DBInterface(db_file)

        balances = iface.getOpenBalances()
        assert balances.__repr__() == "[Balance 2, shared by Dana, Alizée, Loïc, 1 expense(s).]"
