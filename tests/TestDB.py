#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from expense_manager.db import DBInterface

class TestDB:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testFirstTry(self):
        interface = DBInterface("")
        interface.createStructure()
        balances = interface.getOpenBalances()
        print("Begin dump")
        for balance in balances:
            print(balance)
        print("End dump")



