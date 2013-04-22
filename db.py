#!/usr/bin/python
# -*- coding: utf-8 -*-

from .expense import Expense, Balance
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

@sqlalchemy.event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

engine = create_engine('sqlite:///expenses2.db', echo=False)
Base = declarative_base(bind = engine)
Session = sessionmaker(bind=engine)

class DBInterface:

    @staticmethod
    def printExpenses():
        session = Session()
        for expense in session.query(DbExpense).order_by(DbExpense.id):
            print(expense.makeExpense())

    @staticmethod
    def getOpenBalances():
        session = Session()
        open_balances = []
        for balance in session.query(DbBalance).filter(DbBalance.year == None).order_by(DbBalance.id):
            open_balances.append(balance.makeBalance())
        return open_balances

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
