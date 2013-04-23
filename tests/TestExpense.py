#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from expense_manager.core import Expense

class TestExpense:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        self.instance = Expense(2, 2013, 4, 20, "Dana", 10.50, "Trucs...")

    def tearDown(self):
        pass

    def test_constructor(self):

        with assert_raises(TypeError):
            Expense(2, 2013, 4, 20, 123, 10.50, "Trucs")

        with assert_raises(ValueError):
            Expense(2, 2013, 4, 20, "Dana", 10.50, "")

        with assert_raises(ValueError):
            Expense(2, 2013, 4, 20, "", 10.50, "Desc.")

        self.instance.sanityCheck()



