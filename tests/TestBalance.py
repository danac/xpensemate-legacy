#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import assert_equals, assert_raises
from expense_manager.core import Balance, Expense

class TestBalance:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        self.instance = Balance(1, ["Dana", "Alizée", "Mik"], 2013, 2, 10)
        self.instance.sanityCheck()

    def tearDown(self):
        pass

    def test_constructor(self):

        with assert_raises(ValueError):
            Balance(1, ["Dana"], 2013, 2)

        with assert_raises(ValueError):
            Balance(1, [], 2013, 2, 10)

    def test_calculate_empty(self):
        self.instance.calculate()
        self.instance.sanityCheck()

    def test_add_expense(self):
        exp = Expense(2, 2013, 4, 20, "Dana", 10.50, "Trucs...")
        self.instance.addExpense(exp)
        self.instance.sanityCheck()

        with assert_raises(TypeError):
            self.instance.addExpense("coucou")

    def test_add_expense_bad_debtor(self):
        with assert_raises(ValueError):
            exp = Expense(2, 2013, 4, 18, "Loïc", 10.50, "Trucs...")
            self.instance.addExpense(exp)

    def test_calculate(self):
        exp1 = Expense(2, 2013, 4, 20, "Dana", 18, "Trucs...")
        exp2 = Expense(2, 2013, 4, 21, "Mik", 32, "Trucs...")
        exp3 = Expense(2, 2013, 4, 18, "Alizée", 10, "Trucs...")
        self.instance.debtors.append("Loïc")
        self.instance.calculate()
        self.instance.addExpense(exp1)
        self.instance.addExpense(exp2)
        self.instance.addExpense(exp3)
        self.instance.calculate()

        assert self.instance.total == 60
        assert self.instance.average == 15
        assert self.instance.total_delta == 20
        assert self.instance.personal_debts["Dana"] == {}
        assert self.instance.personal_debts["Mik"] == {}
        assert self.instance.personal_debts["Loïc"]["Dana"] == 3/20*15
        assert self.instance.personal_debts["Loïc"]["Mik"] == 17/20*15
        assert self.instance.personal_debts["Alizée"]["Dana"] == 3/20*5
        assert self.instance.personal_debts["Alizée"]["Mik"] == 17/20*5






