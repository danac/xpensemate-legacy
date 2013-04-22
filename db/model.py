#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..expense import Balance, Expense
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

db_template = "sqlite:///expense_manager/db/db_structure.db"
template_engine = create_engine(db_template, echo=False)
Base = declarative_base(bind=template_engine)

def createStructure(engine):
    Base.metadata.create_all(engine)

class DbPerson(Base):
    __tablename__ = "person"
    __table_args__ = {'autoload': True}

class DbExpense(Base):
    __tablename__ = "expense"
    __table_args__ = {'autoload': True}

    buyer = relationship("DbPerson")

    def makeExpense(self):
        return Expense(ID=self.id, year=self.year, month=self.month, day=self.day, buyer=self.buyer.name, amount=self.amount, description=self.description)

class DbBalancePerson(Base):
    __tablename__ = "balance_person"
    __table_args__ = {'autoload': True}

class DbBalance(Base):
    __tablename__ = "balance"
    __table_args__ = {'autoload': True}

    persons = relationship("DbPerson", secondary = DbBalancePerson.__table__)
    expenses = relationship("DbExpense", backref = "balance")

    def makeBalance(self):
        names = []
        for i in self.persons:
            names.append(i.name)
        balance = Balance(ID=self.id, year=self.year, month=self.month, day=self.day, debtors=names)
        for expense in self.expenses:
            balance.addExpense(expense.makeExpense())

        return balance
