#!/usr/bin/python
# -*- coding: utf-8 -*-

from nose.tools import eq_, raises
from expense_manager.core import Expense


class TestExpenseInit:

    @classmethod
    def setupClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInit(self):
        exp = Expense(2, 2013, 4, 20, "Dana", 10.50, "Trucs...")
        exp.sanityCheck()

    @raises(ValueError)
    def testInitBadId(self):
            Expense(0, 2013, 4, 20, "Dana", 10.50, "Trucs...")

    @raises(ValueError)
    def testInitBadYear(self):
        Expense(2, 2012, 4, 20, "Dana", 10.50, "Trucs...")

    @raises(ValueError)
    def testInitBadMonth(self):
        Expense(2, 2013, 0, 20, "Dana", 10.50, "Trucs...")

    @raises(ValueError)
    def testInitBadDay(self):
        Expense(2, 2013, 12, 32, "Dana", 10.50, "Trucs...")

    @raises(TypeError)
    def testInitBadNameType(self):
        Expense(2, 2013, 4, 20, 123, 10.50, "Trucs...")

    @raises(ValueError)
    def testInitEmptyName(self):
        Expense(2, 2013, 4, 20, "", 10.50, "Trucs...")

    @raises(ValueError)
    def testInitBadAmount(self):
        Expense(2, 2013, 4, 20, "Dana", -10.50, "Trucs...")

    @raises(ValueError)
    def testInitNullAmount(self):
        Expense(2, 2013, 4, 20, "Dana", 0, "Trucs...")

    @raises(TypeError)
    def testInitBadDescriptionType(self):
        Expense(2, 2013, 4, 20, "Dana", 0.1, 123)

    @raises(ValueError)
    def testInitEmptyDescription(self):
        Expense(2, 2013, 4, 20, "Dana", 0.1, "")


