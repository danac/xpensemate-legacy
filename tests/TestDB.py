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

    def testQueryOpenBalances(self):
        balances = DBInterface.getOpenBalances()




