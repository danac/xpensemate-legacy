#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import raises, eq_
from expense_manager.core import Balance, Expense

class TestBalanceInit:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInitNoDate(self):
        bal = Balance(1, ["Dana"])
        bal.sanityCheck()

    def testInit(self):
        bal = Balance(1, ["Dana", "Alizée", "Mik"], 2013, 2, 10)
        bal.sanityCheck()

    @raises(ValueError)
    def testInitBadDebtorEmptyList(self):
        Balance(1, [], 2013, 2, 10)

    @raises(TypeError)
    def testInitBadDebtorType(self):
        Balance(1, "Dana", 2013, 2, 10)

    @raises(ValueError)
    def testInitBadDebtorList(self):
        Balance(1, [123], 2013, 2, 10)

    @raises(ValueError)
    def testInitBadId(self):
        Balance(0, ["Dana"], 2013, 2, 10)

    @raises(ValueError)
    def testInitBadYear(self):
        Balance(1, ["Dana"], 2012, 2, 10)

    @raises(ValueError)
    def testInitBadMonth(self):
        Balance(1, ["Dana"], 2012, 13, 10)

    @raises(ValueError)
    def testInitBadDay(self):
        Balance(1, ["Dana"], 2012, 2, 32)

    @raises(ValueError)
    def testInitBadDate(self):
        Balance(1, ["Dana"], 2012, 10)


class TestBalanceMain:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        self.inst = Balance(1, ["Dana", "Alizée", "Mik"], 2013, 2, 10)

    def tearDown(self):
        pass

    def testAddExpense(self):
        exp = Expense(2, 2013, 4, 20, "Dana", 10.50, "Trucs...")
        self.inst.addExpense(exp)

    @raises(TypeError)
    def testAddExpenseBadType(self):
        self.inst.addExpense("coucou")

    @raises(ValueError)
    def testAddExpenseBadDebtor(self):
        exp = Expense(2, 2013, 4, 18, "Loïc", 10.50, "Trucs...")
        self.inst.addExpense(exp)

    def testCalculate_1(self):
        exp1 = Expense(2, 2013, 4, 20, "Dana", 18, "Trucs...")
        exp2 = Expense(2, 2013, 4, 21, "Mik", 32, "Trucs...")
        exp3 = Expense(2, 2013, 4, 18, "Alizée", 10, "Trucs...")
        self.inst.debtors.append("Loïc")
        self.inst.calculate()
        self.inst.addExpense(exp1)
        self.inst.addExpense(exp2)
        self.inst.addExpense(exp3)
        self.inst.calculate()
        self.inst.sanityCheck()

        eq_(self.inst.total, 60)
        eq_(self.inst.average, 15)
        eq_(self.inst.total_delta, 20)
        eq_(self.inst.personal_debts["Dana"], {})
        eq_(self.inst.personal_debts["Mik"], {})
        eq_(self.inst.personal_debts["Loïc"]["Dana"], 3/20*15)
        eq_(self.inst.personal_debts["Loïc"]["Mik"], 17/20*15)
        eq_(self.inst.personal_debts["Alizée"]["Dana"], 3/20*5)
        eq_(self.inst.personal_debts["Alizée"]["Mik"], 17/20*5)

    def testCalculateEmpty(self):
        self.inst.calculate()
        self.inst.sanityCheck()

    def testRepr(self):
        print(self.inst)




