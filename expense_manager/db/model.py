#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..core import Log, Balance, Expense
from .db_helper import UniqueMixin, Base
from sqlalchemy import Column, Integer, ForeignKey, String, Float, Text
from sqlalchemy.orm import relationship

def create_structure(engine):
    Base.metadata.create_all(engine)
    Log.info("Database structure created.")

class DbPerson(UniqueMixin, Base):
    __tablename__ = "person"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50), unique=True)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(DbPerson.name == name)

class DbExpense(Base, Expense):
    __tablename__ = "expense"

    id          = Column("id",          Integer, primary_key = True)
    year        = Column("year",        Integer,                           nullable = False)
    month       = Column("month",       Integer,                           nullable = False)
    day         = Column("day",         Integer,                           nullable = False)
    description = Column("description", Text,                              nullable = False)
    amount      = Column("amount",      Float,                             nullable = False)
    person_id   = Column("person_id",   Integer, ForeignKey("person.id"),  nullable = False)
    balance_id  = Column("balance_id",  Integer, ForeignKey("balance.id"), nullable = False)

    buyer = relationship("DbPerson")

    @staticmethod
    def create(year, month, day, buyer, description, amount, balance_id, session):
        expense = DbExpense()
        expense.year = year
        expense.month = month
        expense.day = day
        expense.description = description
        expense.amount = amount
        expense.buyer = DbPerson.as_unique(session, name = buyer)
        expense.balance_id = balance_id
        return expense

class DbBalancePerson(Base):
    __tablename__ = "balance_person"

    balance_id = Column("balance_id", Integer, ForeignKey("balance.id"), nullable = False, primary_key = True)
    person_id  = Column("person_id",  Integer, ForeignKey("person.id"),  nullable = False, primary_key = True)

class DbBalance(Base, Balance):
    __tablename__ = "balance"

    id    = Column("id",   Integer, primary_key = True)
    year  = Column("year", Integer)
    month = Column("month", Integer)
    day   = Column("day",  Integer)

    persons = relationship("DbPerson", secondary = DbBalancePerson.__table__)
    expenses = relationship("DbExpense")

    @staticmethod
    def create(names, session):
        balance = DbBalance()
        balance.year = None
        balance.month = None
        balance.day = None
        persons = []
        for name in names:
            persons.append(DbPerson.as_unique(session, name = name))
        balance.persons = persons
        
        return balance



