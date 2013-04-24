#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..core import Balance, Expense, Log
from sqlalchemy import Column, Integer, ForeignKey, String, Float, Text, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import inspect, os

Base = declarative_base()

def createStructure(engine):
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
    month       = Column("moth",        Integer,                           nullable = False)
    day         = Column("day",         Integer,                           nullable = False)
    description = Column("description", Text,                              nullable = False)
    amount      = Column("amount",      Float,                             nullable = False)
    person_id   = Column("person_id",   Integer, ForeignKey("person.id"),  nullable = False)
    balance_id  = Column("balance_id",  Integer, ForeignKey("balance.id"), nullable = False)

    buyer = relationship("DbPerson")
    balance = relationship("DbBalance")

    def makeExpense(self):
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
    month = Column("moth", Integer)
    day   = Column("day",  Integer)

    persons = relationship("DbPerson", secondary = DbBalancePerson.__table__)
    expenses = relationship("DbExpense")

    def makeBalance(self):
        names = []
        for i in self.persons:
            names.append(i.name)
        balance = Balance(ID=self.id, year=self.year, month=self.month, day=self.day, debtors=names)
        for expense in self.expenses:
            balance.addExpense(expense.makeExpense())

        Log.debug("Made a balance: {}".format(balance))
        return balance

