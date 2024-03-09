import dataoperator
from client import Client
import timekeeper
from plan import Plan, DepositPlan, CreditPlan
from dataoperator import put, get

class Account:
    __id: int # PK
    __owner: int
    __opened: bool  # todo: action blocking decorator
    __money: float

    def __init__(self, owner):
        self.__owner = owner
        self.__opened = True
        self.__money = 0
        self.__id = dataoperator.put(self)

class DebitAccount(Account):

    def put(self, cash: float) -> bool:
        if cash < 0:
            return False
        self.__money += cash
        return True

    def get(self, amount: float) -> bool:
        if amount > 0 and self.__money >= amount:
            self.__money -= amount
            return True
        return False

class DepositAccount(Account):
    __plan: DepositPlan
    __freeze_date: int

    def __init__(self, owner: int, plan: DepositPlan):
        super().__init__(owner)
        self.__plan = plan
        self.__freeze_date = timekeeper.get() + plan.__period

    def update(self):
        modifier = 1 + self.__plan.get_commission()
        if dataoperator.get(self.__owner, Client).is_precarious():
            modifier += self.__plan.get_penalty()
        self.__money *= modifier ** (timekeeper.get() - self.__freeze_date)

    def put(self, cash: float) -> bool:
        if cash < 0:
            return False
        self.__money += cash
        return True

    def get(self, amount: float) -> bool:
        if amount > 0 and self.__money >= amount and self.__freeze_date >= timekeeper.get():
            self.__money -= amount
            return True
        return False

class CreditAccount(Account):
    __plan: CreditPlan

    def __init__(self, owner: int, plan: CreditPlan):
        super().__init__(owner)
        self.__plan = plan
        self.__freeze_date = timekeeper.get() + plan.__period

    def update(self):
        if self.__money >= 0:
            pass
        modifier = 1 + self.__plan.get_commission()
        if dataoperator.get(self.__owner, Client).is_precarious():
            modifier += self.__plan.get_penalty()
        self.__money *= modifier

    def put(self, cash: float) -> bool:
        if cash < 0:
            return False
        self.__money += cash
        return True

    def get(self, amount: float) -> bool:
        if self.__money - amount < self.__plan.__limit:
            return False
        self.__money -= amount
        return True
