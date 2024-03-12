from typing import List, Optional
from plan import Plan, DepositPlan, CreditPlan
import dataoperator
from account import Account, DepositAccount, CreditAccount, DebitAccount
from transaction import Transaction
from accountfactory import AccountFactory
from clientbuilder import ClientBuilder


class Bank:
    '''У банка есть привязанные к нему планы, счета и клиенты.
    На среднем уровне взаимодействие происходит через него.'''

    __id: int # PK
    __name: str
    __clients: List[int]
    __accounts: List[int]
    __plans: List[int]
    __registrator: ClientBuilder

    def __init__(self, name: str):
        self.__clients = []
        self.__accounts = []
        self.__plans = []
        self.__name = name
        self.__registrator = ClientBuilder()
        from dataoperator import DataOperator
        self.__id = DataOperator().put(self)

    @property
    def id(self):
        return self.__id

    def register(self, name: str, surname: str, address: Optional[str] = None, passport: Optional[int] = None) -> Optional[int]:
        for id in self.__clients:
            from dataoperator import DataOperator
            client = DataOperator().get(id, "Client")
            if client.name == name and client.surname == surname:
                return None
        self.__registrator.reset(name, surname)
        if address is not None:
            self.__registrator.address(address)
        if passport is not None:
            self.__registrator.passport(passport)
        client = self.__registrator.get().id
        self.__clients.append(client)
        return client

    def add_plan(self, plan: Plan) -> Optional[int]:
        for id in self.__plans:
            if id == plan.id:
                return None
        self.__plans.append(plan.id)
        return plan.id

    def open_account(self, owner: int, plan: int) -> Optional[int]:
        if not owner in self.__clients or not plan in self.__plans:
            return None
        from dataoperator import DataOperator
        plan_obj = DataOperator().get(plan, "Plan")
        acc = AccountFactory.create(owner, plan_obj).id
        self.__accounts.append(acc)
        return acc

    def transfer(self, departure: int, destination: int, amount: int) -> bool:
        if not departure in self.__accounts or not destination in self.__accounts:
            return False
        from dataoperator import DataOperator
        dep: Account = DataOperator().get(departure, "Account")
        dest: Account = DataOperator().get(destination, "Account")
        trans = Transaction(departure, destination, amount)
        if dep.get_offer(amount) and dest.put_offer(amount):
            dep.get(amount)
            dest.put(amount)
            trans.prove()
            return True
        trans.cancel()
        return False

    def get(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        from dataoperator import DataOperator
        dep = DataOperator().get(account, "Account")
        trans = Transaction(0, account, amount)
        if dep.get_offer(amount):
            dep.get(amount)
            trans.prove()
            return True
        else:
            trans.cancel()
            return False

    def put(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        from dataoperator import DataOperator
        dest = DataOperator().get(account, "Account")
        trans = Transaction(account, 0, amount)
        if dest.put_offer(amount):
            dest.put(amount)
            trans.prove()
            return True
        else:
            trans.cancel()
            return False

    def update(self, owner: int, address: str, passport: int) -> bool:
        if owner not in self.__clients:
            return False
        else:
            from dataoperator import DataOperator
            DataOperator().get(owner, "Client").update(address, passport)

