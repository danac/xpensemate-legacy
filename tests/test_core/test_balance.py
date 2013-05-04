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
        bal = Balance(["Dana"])
        bal.sanity_check()

    def testInit(self):
        bal = Balance(["Dana", "Alizée", "Mik"], 2013, 2, 10)
        bal.sanity_check()

    @raises(ValueError)
    def testInitBadDebtorEmptyList(self):
        Balance([], 2013, 2, 10)

    @raises(TypeError)
    def testInitBadDebtorType(self):
        Balance("Dana", 2013, 2, 10)

    @raises(TypeError)
    def testInitBadDebtorList(self):
        Balance([123], 2013, 2, 10)

    #@raises(ValueError)
    #def testInitBadId(self):
        #Balance(0, ["Dana"], 2013, 2, 10)

    @raises(ValueError)
    def testInitBadYear(self):
        Balance(["Dana"], 2012, 2, 10)

    @raises(ValueError)
    def testInitBadMonth(self):
        Balance(["Dana"], 2012, 13, 10)

    @raises(ValueError)
    def testInitBadDay(self):
        Balance(["Dana"], 2012, 2, 32)

    @raises(ValueError)
    def testInitBadDate(self):
        Balance(["Dana"], 2012, 10)


class TestBalanceMain:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        self.inst = Balance(["Dana", "Alizée", "Mik"], 2013, 2, 10)

    def tearDown(self):
        pass

    def testadd_expense(self):
        exp = Expense(2013, 4, 20, "Dana", 10.50, "Trucs...")
        self.inst.add_expense(exp)

    @raises(TypeError)
    def testadd_expenseBadType(self):
        self.inst.add_expense("coucou")

    @raises(ValueError)
    def testadd_expenseBadDebtor(self):
        exp = Expense(2013, 4, 18, "Loïc", 10.50, "Trucs...")
        self.inst.add_expense(exp)

    def testCalculate_1(self):
        exp1 = Expense(2013, 4, 20, "Dana", 18, "Trucs...")
        exp2 = Expense(2013, 4, 21, "Mik", 32, "Trucs...")
        exp3 = Expense(2013, 4, 18, "Alizée", 10, "Trucs...")
        self.inst.debtors.append("Loïc")
        self.inst.calculate()
        self.inst.add_expense(exp1)
        self.inst.add_expense(exp2)
        self.inst.add_expense(exp3)
        self.inst.calculate()
        self.inst.sanity_check()

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
        self.inst.sanity_check()

    def testRepr(self):
        print(self.inst)
        print(self.inst.__repr__(dump=True))

