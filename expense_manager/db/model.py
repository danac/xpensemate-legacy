#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..core import Balance, Expense, Log
from sqlalchemy import Column, Integer, ForeignKey, String, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def create_structure(engine):
    Base.metadata.create_all(engine)
    Log.info("Database structure created.")

class DbPerson(Base):
    __tablename__ = "person"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50))

class DbExpense(Base):
    __tablename__ = "expense"

    id          = Column("id",          Integer, primary_key = True)
    year        = Column("year",        Integer,                           nullable = False)
    month       = Column("month",        Integer,                           nullable = False)
    day         = Column("day",         Integer,                           nullable = False)
    description = Column("description", Text,                              nullable = False)
    amount      = Column("amount",      Float,                             nullable = False)
    person_id   = Column("person_id",   Integer, ForeignKey("person.id"),  nullable = False)
    balance_id  = Column("balance_id",  Integer, ForeignKey("balance.id"), nullable = False)

    buyer = relationship("DbPerson")
    balance = relationship("DbBalance")

    def from_expense(self, expense, balance):
        self.year = expense.year
        self.month = expense.month
        self.day = expense.day
        self.description = expense.description
        self.buyer = DbPerson(name = expense.buyer)
        self.description = expense.description
        self.amount = expense.amount
        self.balance = balance

    def make_expense(self):
        expense = Expense(
            ID          = self.id,
            year        = self.year,
            month       = self.month,
            day         = self.day,
            buyer       = self.buyer.name,
            amount      = self.amount,
            description = self.description )
        Log.debug("Made an expense: {}".format(expense))
        return expense

class DbBalancePerson(Base):
    __tablename__ = "balance_person"

    balance_id = Column("balance_id", Integer, ForeignKey("balance.id"), nullable = False, primary_key = True)
    person_id  = Column("person_id",  Integer, ForeignKey("person.id"),  nullable = False, primary_key = True)

class DbBalance(Base):
    __tablename__ = "balance"

    id    = Column("id",   Integer, primary_key = True)
    year  = Column("year", Integer)
    month = Column("month", Integer)
    day   = Column("day",  Integer)

    persons = relationship("DbPerson", secondary = DbBalancePerson.__table__)
    expenses = relationship("DbExpense")

    def make_balance(self):
        names = []
        for i in self.persons:
            names.append(i.name)
        balance = Balance(ID=self.id, year=self.year, month=self.month, day=self.day, debtors=names)
        for expense in self.expenses:
            balance.add_expense(expense.make_expense())

        Log.debug("Made a balance: {}".format(balance))
        return balance

    def from_balance(self, balance):
        self.year = balance.year
        self.month = balance.month
        self.day = balance.day
        persons = []
        for name in balance.debtors:
            persons.append(DbPerson(name=name))
        self.persons = persons

