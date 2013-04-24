#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pformat
from .common import Log, Constants

class Expense:

    def __init__(self, ID, year, month, day, buyer, amount, description):
        self.ID          = int(ID)
        self.year        = int(year)
        self.month       = int(month)
        self.day         = int(day)
        self.buyer       = buyer
        self.amount      = float(amount)
        self.description = description

        self.valueCheck()

    def sanityCheck(self):

        assert type(self.ID) is int, (
            "L'identifiant de dépense \"{}\" n'a pas le bon type "
                .format(self.ID) +
            "(devrait être \"{}\" au lieu de \"{}\")."
                .format(int, type(self.ID)) )

        assert self.ID > 0, ( "L'identifiant de dépense \"{}\" n'est pas admissible."
                             .format(self.ID) )

        self.valueCheck()

    def valueCheck(self):

        if not type(self.year) is int:
            raise TypeError("Année invalide.")

        if not self.year >= Constants.MIN_YEAR:
            raise ValueError("Année invalide.")

        if not type(self.month) is int:
            raise TypeError("Mois invalide.")

        if not self.month > 0 and self.month <= 12:
            raise ValueError("Mois invalide.")

        if not type(self.day) is int:
            raise TypeError("Jour du mois invalide.")

        if not self.day > 0 and self.day <= 31:
            raise ValueError("Jour du mois invalide.")

        if type(self.description) is not str:
            raise TypeError("Description invalide.")

        if self.description == "":
            raise ValueError("Description invalide.")

        if type(self.buyer) is not str:
            raise TypeError("Nom invalide.")

        if self.buyer == "":
            raise ValueError("Nom invalide.")

        if type(self.amount) is not float and type(self.amount) is not int:
            raise TypeError("Montant invalide (type \"{}\".".format(type(self.amount)))

        if not self.amount > 0:
            raise ValueError("Montant invalide.")

        date_fields = [self.day, self.month, self.year]
        if not ( all(i is None for i in date_fields) or
                 all(i is not None for i in date_fields) ):
            message = "Date inconsistente.."
            raise ValueError(message)

    def __repr__(self, indent = 0):
        description = ' '*indent
        description += ( "Expense {ID}, {amount} by {buyer} on {year}-{month:02}-{day:02}."
            .format(**self.__dict__) )
        return description

class Balance:
    def __init__(self, ID, debtors, year = None, month = None, day = None):
        self.ID       = ID
        self.year     = year
        self.month    = month
        self.day      = day
        self.expenses = []
        self.debtors  = debtors

        self.average = 0.0
        self.total = 0.0
        self.total_delta = 0.0
        self.personal_paid = {}
        self.personal_diff = {}
        self.personal_debts = {}

        self.reset()
        self.valueCheck()

    def reset(self):
        self.average = 0.0
        self.total = 0.0
        self.total_delta = 0.0

        self.personal_paid = {}
        self.personal_diff = {}
        self.personal_debts = {}

        for debtor in self.debtors:
            self.personal_paid[debtor] = 0.0
            self.personal_diff[debtor] = 0.0
            self.personal_debts[debtor] = {}

    def calculate(self):
        self.reset()

        for expense in self.expenses:
            self.total += expense.amount
            self.personal_paid[expense.buyer] += expense.amount

        self.average = self.total / len(self.debtors)

        for debtor in self.debtors:
            self.personal_diff[debtor] = self.personal_paid[debtor]-self.average
            if self.personal_diff[debtor] > 0:
                self.total_delta += self.personal_diff[debtor]

        for payer in self.debtors:
            if self.personal_diff[payer] < 0 and self.total_delta != 0.0:
                debt = {}
                receivers = [debtor for debtor in self.debtors if self.personal_diff[debtor] > 0]
                for receiver in receivers:
                    ratio = self.personal_diff[receiver] / self.total_delta
                    debt[receiver] = abs(self.personal_diff[payer]) * ratio
                self.personal_debts[payer] = debt

    def valueCheck(self):

        if not len(self.debtors) > 0:
            raise ValueError("Aucun débiteur.")

        for debtor in self.debtors:
            if not type(debtor) is str:
                message = "Le débiteur \"{}\" n'a pas le bon type ".format(debtor)
                "(devrait être \"{}\" au lieu de \"{}\")".format(str, type(debtor))
                raise ValueError(message)

        date_fields = [self.day, self.month, self.year]
        if not ( all(i is None for i in date_fields) or
                 all(i is not None for i in date_fields) ):
            message = "Date de clôture inconsistente.."
            raise ValueError(message)

        if self.day is not None:
            if not (self.day > 0 and self.day <= 31):
                message = "Jour invalide."
                raise ValueError(message)
            if not (self.month > 0 and self.month <= 12):
                message = "Mois invalide."
                raise ValueError(message)
            if not (self.year >= Constants.MIN_YEAR):
                message = "Année invalide."
                raise ValueError(message)

            if type(self.day) is not int:
                raise TypeError("Jour invalide (type \"{}\"".format(type(self.day)))
            if type(self.year) is not int:
                raise TypeError("Année invalide (type \"{}\"".format(type(self.year)))
            if type(self.month) is not int:
                raise TypeError("Mois invalide (type \"{}\"".format(type(self.month)))


    def sanityCheck(self):

        assert type(self.ID) is int, (
            "L'identifiant de bilan \"{}\" n'a pas le bon type "
                .format(self.ID) +
            "(devrait être \"{}\" au lieu de \"{}\")"
                .format(int, type(self.ID)) )

        assert self.ID > 0, (
            "L'identifiant de bilan \"{}\" n'est pas admissible."
                .format(self.ID) )

        for debtor in self.debtors:
            assert type(debtor) is str, (
                "Le débiteur \"{}\" du bilan \"{}\" n'a pas le bon type "
                    .format(debtor, self.ID) +
                "(devrait être \"{}\" au lieu de \"{}\")"
                    .format(str, type(debtor)) )

            assert debtor in self.personal_paid, (
                "Le débiteur \"{}\" n'est pas dans les paiements du bilan \"{}\""
                    .format(debtor, self.ID) )

            assert debtor in self.personal_diff, (
                "Le débiteur \"{}\" n'est pas dans les écarts à la moyenne du bilan \"{}\""
                    .format(debtor, self.ID) )

            assert debtor in self.personal_debts, (
                "Le débiteur \"{}\" n'est pas dans les dettes du bilan \"{}\""
                    .format(debtor, self.ID) )

        self.valueCheck()

        test_total = 0.0
        for expense in self.expenses:
            assert type(expense) is Expense, (
                "La dépense \"{}\" n'est pas du bon type (type \"{}\")"
                    .format(self.ID, type(expense)) )
            try:
                expense.sanityCheck()
            except ValueError as err:
                raise ValueError(
                    "La dépense \"{}\" dans le bilan \"{}\" n'est pas valable.\n"
                        .format(expense.ID, self.ID) +
                    err.message )

            if expense.buyer not in self.debtors:
                raise ValueError(
                    "Le nom \"{}\" n'est pas inscrit au bilan (dépense \"{}\")."
                        .format(expense.buyer, expense.description) )

            test_total += expense.amount

        assert test_total == self.total, (
            "Le montant total dans le bilan \"{}\" est faux "
                .format(self.ID) +
            "(devrait être \"{}\" au lieu de \"{}\")."
                .format(test_total, self.total) )

        assert len(self.debtors) > 0, (
            "Aucun débiteur dans le bilan \"{}\"!".format(self.ID) )

        assert self.average == self.total / len(self.debtors), (
            "Le montant moyen par personne dans le bilan \"{}\" est faux "
                .format(self.ID) +
             "(devrait être \"{}\" au lieu de \"{}\")."
                .format(self.total / len(self.debtors), self.average) )

        for key in self.personal_paid:
            assert key in self.debtors, (
                "La personne \"{}\" (dans les paiements du bilan \"{}\") n'est pas inscrite au bilan."
                    .format(key, self.ID) )

        for key in self.personal_diff:
            assert key in self.debtors, (
                "La personne \"{}\" (dans les écarts à la moyenne du bilan \"{}\") n'est pas inscrite au bilan."
                    .format(key, self.ID) )

            assert self.personal_diff[key] == self.personal_paid[key] - self.average, (
                "La différence à la moyenne du débiteur \"{}\"  dans le bilan \"{}\" est fausse "
                    .format(key, self.ID) +
                "(devrait être \"{}\" au lieu de \"{}\")."
                    .format(self.personal_paid[key] - self.average[key], self.personal_diff[key]) )

        for payer in self.personal_debts:
            assert payer in self.debtors, (
                "La personne \"{}\" (dans la liste des dettes du bilan \"{}\") n'est pas inscrite au bilan."
                    .format(payer, self.ID) )
            assert type(self.personal_debts[payer]) is dict, (
                "La liste de dettes de \"{}\" dans le bilan \"{}\" a un type invalide "
                    .format(payer, self.ID) +
                "(devrait être \"{}\" au lieu de \"{}\")"
                    .format(dict, type(self.personal_debts[payer])) )

            if len(self.personal_debts[payer]) != 0:
                for receiver in self.personal_debts[payer] :
                    if receiver == payer:
                        continue
                    assert receiver in self.debtors, (
                        "La personne \"{}\" (dans les dettes de \"{}\" dans le bilan \"{}\") n'est pas inscrite au bilan."
                            .format(receiver, payer, self.ID) )

                    debt = self.personal_debts[payer][receiver]
                    assert type(debt) is float, (
                        "La dette de \"{}\" envers \"{}\" dans le bilan \"{}\" a un type invalide "
                            .format(payer, receiver, self.ID) +
                        "(devrait être \"{}\" au lieu de \"{}\")"
                            .format(float, type(debt)) )

                    assert debt > 0.0, (
                        "La dette de \"{}\" envers \"{}\" dans le bilan \"{}\" n'est pas positive."
                            .format(payer, receiver, self.ID) )

        Log.debug("BALANCE {} checked for sanity! Summary: ".format(self.ID))
        Log.debug("Total amount: " + pformat(self.total))
        Log.debug("Average amount: " + pformat(self.average))
        Log.debug("Total delta: " + pformat(self.total_delta))
        Log.debug("Diffs: " + pformat(self.personal_diff))
        Log.debug("Debts: " + pformat(self.personal_debts))

    def addExpense(self, expense):

        if type(expense) is not Expense:
            message = ( "Type de dépense inconnu (type \"{}\")."
                .format(type(expense)) )
            raise TypeError(message)

        if expense.buyer not in self.debtors:
            raise ValueError(
                "Le nom \"{}\" n'est pas inscrit au bilan."
                    .format(expense.buyer, expense.description) )

        self.expenses.append(expense)
        self.calculate()

    def __repr__(self, indent = 0, dump = False):
        indentation = indent
        description = "Balance {}, shared by {}".format(self.ID, ', '.join(self.debtors))
        if(self.day is not None):
            description += " closed on {year}-{month:02}-{day:02}".format(**self.__dict__)
        if len(self.expenses) == 0:
            description += ' '*indentation + ", no expense."
        else:
            if dump:
                description += ":\n"
                for expense in self.expenses:
                    description += expense.__repr__(indentation)

            else:
                description += ' '*indentation + ", {} expense(s).".format(len(self.expenses))

        return description

class ExpenseManager:
    def __init__(self):
        self.open_balances = []
        self.db_connection = DBInterface()

    def loadFromDB(self):
        pass

    def addOpenBalance(self, balance):
        assert type(balance) is Balance, (
            "Type de bilan inconnu (type \"{}\")."
                .format(type(expense)) )

        open_balances.append(balance)

    def sanityCheck(self):
        for balance in self.open_balances:
            assert type(balance) is Balance, (
                "Type de bilan inconnu (type \"{}\")."
                    .format(type(expense)) )
            balance.sanityCheck()




