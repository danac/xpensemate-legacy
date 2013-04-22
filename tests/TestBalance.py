#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from expense_manager.expense import Balance, Expense

class TestBalance:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        self.instance = Balance(1, ["Dana"], 2013, 2, 10)

    def tearDown(self):
        pass

    def test_constructor(self):

        with assert_raises(TypeError):
            Balance(1, ["Dana"], 2013, 2)

        with assert_raises(ValueError):
            Balance(1, [], 2013, 2, 10)

    def test_calculate_empty(self):
        self.instance.calculate()
        self.instance.sanityCheck()

    def test_add_expense(self):
        exp = Expense(2, 2013, 4, 20, "Dana", 10.50, "Trucs...")
        self.instance.addExpense(exp)

        with assert_raises(TypeError):
            self.instance.addExpense("coucou")




