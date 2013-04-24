#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from expense_manager.db import DBInterface
import shutil

class TestDBSQLite:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        self.interface_memory = DBInterface("")
        pass

    def tearDown(self):
        pass

    def test_structure(self):
        self.interface_memory.createStructure()

    def test_add_query_expense(self):
        pass

    def test_query_open_balance(self):
        pass

