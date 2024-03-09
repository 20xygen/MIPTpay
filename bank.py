from typing import Dict, List, Optional
from plan import Plan, DepositPlan, CreditPlan
import dataoperator
from client import Client
from account import Account, DepositAccount, CreditAccount
from transaction import Transaction
from dataoperator import get, put

class Bank:
    __id: int # PK
    __name: str
    __clients: List[int]
    __accounts: List[int]
    __plans: List[int]

    @property
    def id(self):
        return self.__id

    def register(self, name: str, surname: str, address: Optional[str] = None, passport: Optional[int] = None) -> bool:
        for id in self.__clients:
            client = dataoperator.get(id, Client)
            if client.name == name and client.surname == surname:
                return False
        self.__clients.append(Client(name, surname, address, passport).id)

    def add_plan(self, plan: Plan):
        for id in self.__plans:
            if id == plan.id:
                return False

    def open_account(self, owner: int, plan: Optional[int] = None) -> Optional[int]:
        if not plan is None:
            if not owner in self.__clients or not plan in self.__plans:
                return None
            if isinstance(plan, CreditPlan):
                self.__accounts.append(CreditAccount(owner, plan).id)
            elif isinstance(plan, DepositPlan):
                self.__accounts.append(DepositAccount(owner, plan).id)
            else:
                return None
        else:
            if not owner in self.__clients:
                return None
            self.__accounts.append(Account(owner).id)

    def transfer(self, departure: int, destination: int, amount: int) -> bool:
        if not departure in self.__accounts or not destination in self.__accounts:
            return False
        dep: Account = dataoperator.get(departure, Account)
        dest: Account = dataoperator.get(destination, Account)
        trans = Transaction(departure, destination, amount)
        if dep.get_offer(amount) and dest.put_offer(amount):
            dep.get(amount)
            dep.put(amount)
            trans.prove()
            return True
        trans.cancel()
        return False

    def get(self, account: int, amount: int) -> bool:
        if not account in self.__accounts:
            return False
        dep = dataoperator.get(account, Account)
        trans = Transaction(0, account, amount)
        if dep.get_offer(amount):
            dep.get(account)
            trans.prove()
            return True
        else:
            trans.cancel()
            return False

    def put(self, account: int, amount: int) -> bool:
        if not account in self.__accounts:
            return False
        dest = dataoperator.get(account, Account)
        trans = Transaction(account, 0, amount)
        if dest.put_offer(amount):
            dest.put(account)
            trans.prove()
            return True
        else:
            trans.cancel()
            return False
