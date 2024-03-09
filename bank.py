from typing import List, Optional
from plan import Plan, DepositPlan, CreditPlan
import dataoperator
from client import Client
from account import Account, DepositAccount, CreditAccount, DebitAccount
from transaction import Transaction


class Bank:
    __id: int # PK
    __name: str
    __clients: List[int]
    __accounts: List[int]
    __plans: List[int]

    def __init__(self, name: str):
        self.__clients = []
        self.__accounts = []
        self.__plans = []
        self.__name = name
        self.__id = dataoperator.put(self)

    @property
    def id(self):
        return self.__id

    def register(self, name: str, surname: str, address: Optional[str] = None, passport: Optional[int] = None) -> Optional[int]:
        for id in self.__clients:
            client = dataoperator.get(id, "Client")
            if client.name == name and client.surname == surname:
                return None
        client = Client(name, surname, address, passport).id
        self.__clients.append(client)
        return client

    def add_plan(self, plan: Plan) -> Optional[int]:
        for id in self.__plans:
            if id == plan.id:
                return None
        self.__plans.append(plan.id)
        return plan.id

    def open_account(self, owner: int, plan: Optional[int] = None) -> Optional[int]:
        if not plan is None:
            if not owner in self.__clients or not plan in self.__plans:
                return None
            plan_obj = dataoperator.get(plan, "Plan")
            if isinstance(plan_obj, CreditPlan):
                acc = CreditAccount(owner, plan).id
                self.__accounts.append(acc)
            elif isinstance(plan_obj, DepositPlan):
                acc = DepositAccount(owner, plan).id
                self.__accounts.append(acc)
            else:
                return None
        else:
            if not owner in self.__clients:
                return None
            acc = DebitAccount(owner).id
            self.__accounts.append(acc)
        return acc

    def transfer(self, departure: int, destination: int, amount: int) -> bool:
        if not departure in self.__accounts or not destination in self.__accounts:
            return False
        dep: Account = dataoperator.get(departure, "Account")
        dest: Account = dataoperator.get(destination, "Account")
        trans = Transaction(departure, destination, amount)
        if dep.get_offer(amount) and dest.put_offer(amount):
            dep.get(amount)
            dest.put(amount)
            trans.prove()
            return True
        trans.cancel()
        return False

    def get(self, account: int, amount: int) -> bool:
        if not account in self.__accounts:
            return False
        dep = dataoperator.get(account, "Account")
        trans = Transaction(0, account, amount)
        if dep.get_offer(amount):
            dep.get(amount)
            trans.prove()
            return True
        else:
            trans.cancel()
            return False

    def put(self, account: int, amount: int) -> bool:
        if not account in self.__accounts:
            return False
        dest = dataoperator.get(account, "Account")
        trans = Transaction(account, 0, amount)
        if dest.put_offer(amount):
            dest.put(amount)
            trans.prove()
            return True
        else:
            trans.cancel()
            return False
