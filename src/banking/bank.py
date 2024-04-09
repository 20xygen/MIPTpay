from typing import List, Optional
import re
from inspect import currentframe as cf
import src


class Bank:
    """ The banking has plans, accounts and clients linked to it.
    At the middle level, the interaction takes place through it. """

    __id: int # PK
    __name: str
    __clients: List[int]
    __accounts: List[int]
    __plans: List[int]
    __registrator: src.ClientBuilder

    def __init__(self, name: str):
        self.__clients = []
        self.__accounts = []
        self.__plans = []
        self.__name = name
        self.__registrator = src.ClientBuilder()
        self.__id = src.DataOperator().put(self, False)

    def __init__(self, ident: int, name: str, clients: List[int], accounts: List[int], plans: List[int]):
        src.available_from(cf())  # not available for non-gods
        self.__id = ident
        self.__name = name
        self.__clients = clients
        self.__accounts = accounts
        self.__plans = plans
        self.__registrator = src.ClientBuilder()

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def plans(self):
        return self.__plans

    @property
    def accounts(self):
        return self.__accounts

    @property
    def clients(self):
        return self.__clients

    def register(self, name: str, surname: str, address: Optional[str] = None, passport: Optional[str] = None) -> Optional[int]:
        # for id in self.__clients:
        #     client = src.DataOperator().get(id, "Client")
        #     if client.name == name and client.surname == surname:
        #         return None
        pattern = re.compile("\d{10}")
        if passport is not None:
            passport = passport.replace(" ", "")
            if not pattern.match(passport):
                return None
        self.__registrator.reset(name, surname)
        if address is not None:
            self.__registrator.address(address)
        if passport is not None:
            self.__registrator.passport(passport)
        client = self.__registrator.get().id
        if client is None:
            return None
        self.__clients.append(client)
        src.DataOperator().done_with(client, "Client")
        return client

    def add_plan(self, plan: int) -> Optional[int]:
        # for id in self.__plans:
        #     if id == plan.id:
        #         return None
        self.__plans.append(plan)
        # src.DataOperator().done_with(plan.id, "Plan")
        return plan

    def open_account(self, owner: int, plan: int) -> Optional[int]:
        if not owner in self.__clients or not plan in self.__plans:
            print(owner, self.__clients, plan, self.__plans)
            return None
        plan_obj = src.DataOperator().get(plan, "Plan")
        if plan_obj is None:
            return None
        acc = src.AccountFactory.create(owner, plan_obj).id
        self.__accounts.append(acc)
        # src.DataOperator().done_with(acc, "Account")
        src.DataOperator().done_with(plan, "Plan")
        return acc

    def transfer(self, departure: int, destination: int, amount: int) -> bool:
        if not departure in self.__accounts or not destination in self.__accounts:
            return False
        dep: src.Account = src.DataOperator().get(departure, "Account")
        dest: src.Account = src.DataOperator().get(destination, "Account")
        if dest is None or dep is None:
            return False
        trans = src.Transaction(departure, destination, amount)
        if dep.get_offer(amount) and dest.put_offer(amount):
            dep.get(amount)
            dest.put(amount)
            trans.prove()
            src.DataOperator().done_with(dep.id, "Account")
            src.DataOperator().done_with(dest.id, "Account")
            src.DataOperator().done_with(trans.id, "Transaction")
            return True
        trans.cancel()
        src.DataOperator().done_with(dep.id, "Account")
        src.DataOperator().done_with(dest.id, "Account")
        src.DataOperator().done_with(trans.id, "Transaction")
        return False

    def do_get(self, account: int, amount: float):
        src.available_from(cf(), "CrossPaymentSystem")
        dep = src.DataOperator().get(account, "Account")
        if dep is None:
            src.DataOperator().done_with(account, "Account")
            return None
        src.DataOperator().done_with(account, "Account")
        dep.get(amount)

    def do_put(self, account: int, amount: float):
        src.available_from(cf(), "CrossPaymentSystem")
        dep = src.DataOperator().get(account, "Account")
        if dep is None:
            src.DataOperator().done_with(account, "Account")
            return None
        src.DataOperator().done_with(account, "Account")
        dep.put(amount)

    def get(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        dep = src.DataOperator().get(account, "Account")
        if dep is None:
            return False
        trans = src.Transaction(0, account, amount)
        if dep.get_offer(amount):
            self.do_get(account, amount)
            trans.prove()
            src.DataOperator().done_with(trans.id, "Transaction")
            src.DataOperator().done_with(dep.id, "Account")
            return True
        else:
            trans.cancel()
            src.DataOperator().done_with(trans.id, "Transaction")
            src.DataOperator().done_with(dep.id, "Account")
            return False

    def put(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        dest = src.DataOperator().get(account, "Account")
        if dest is None:
            # src.DataOperator().done_with(dest.id, "Account")
            return False
        trans = src.Transaction(account, 0, amount)
        # src.DataOperator().put(trans)
        if dest.put_offer(amount):
            self.do_put(account, amount)
            trans.prove()
            src.DataOperator().done_with(trans.id, "Transaction")
            src.DataOperator().done_with(dest.id, "Account")
            return True
        else:
            trans.cancel()
            src.DataOperator().done_with(trans.id, "Transaction")
            src.DataOperator().done_with(dest.id, "Account")
            return False

    def update(self, owner: int, address: str, passport: str) -> bool:
        pattern = re.compile("\d{10}")
        if passport is not None:
            passport = passport.replace(" ", "")
            if not pattern.match(passport):
                return False
        if owner not in self.__clients:
            return False
        else:
            client_obj = src.DataOperator().get(owner, "Client")
            if client_obj is None:
                src.DataOperator().done_with(owner, "Client")
                return False
            client_obj.update(address, passport)
            src.DataOperator().done_with(owner, "Client")

    def valid_client(self, account: int, client: int) -> bool:
        if client not in self.__clients:
            return False
        account_obj = src.DataOperator().get(account, "Account")
        ret = False
        if account_obj is not None:
            ret = account_obj.owner == client
        src.DataOperator().done_with(account, "Account")
        return ret

    def get_offer(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        account_obj = src.DataOperator().get(account, "Account")
        ret = False
        if account_obj is not None:
            ret = account_obj.get_offer(amount)
        src.DataOperator().done_with(account, "Account")
        return ret

    def put_offer(self, account: int, amount: float) -> bool:
        if not account in self.__accounts:
            return False
        account_obj = src.DataOperator().get(account, "Account")
        ret = False
        if account_obj is not None:
            ret = account_obj.put_offer(amount)
        src.DataOperator().done_with(account, "Account")
        return ret
