import dataoperator
import timekeeper
from plan import DepositPlan, CreditPlan


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
        timekeeper.add(self.__id)

    def put(self, cash: float) -> int:
        self.__money += cash
        return self.__id

    def get(self, cash: float) -> int:
        self.__money -= cash
        return self.__id

    @property
    def id(self):
        return self.__id

    @property
    def opened(self):
        return self.__opened

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, money):
        self.__money = money

    @property
    def owner(self):
        return self.__owner

    def put_offer(self, cash: float) -> bool:
        if cash < 0:
            return False
        # self.__money += cash
        return True

    def get_offer(self, amount: float) -> bool:
        if amount > 0 and self.__money >= amount:
            # self.__money -= amount
            return True
        return False

    def update(self):
        pass

    def info(self) -> str:
        st = str(self.id) + ("(open)" if self.opened else "(closed)") + '\n'
        owner_obj = dataoperator.get(self.owner, "Client")
        st += f"Owner: {owner_obj.name} {owner_obj.surname}\n"
        st += ("Precarious" if owner_obj.precarious else "Not precarious") + f": {owner_obj.address} {owner_obj.passport}\n"
        st += str(self.money) + "\n"
        return st

class DebitAccount(Account):
    def __init__(self, owner: int):
        super().__init__(owner)
        # self.__id = dataoperator.put(self)


class DepositAccount(Account):
    __plan: int
    __freeze_date: int

    @property
    def plan(self):
        return self.__plan

    @property
    def freeze_date(self):
        return self.__freeze_date

    def __init__(self, owner: int, plan: int):
        super().__init__(owner)
        self.__plan = plan
        plan_obj = dataoperator.get(plan, "Plan")
        self.__freeze_date = timekeeper.get()
        # self.__id = dataoperator.put(self)

    def update(self):
        plan_obj = dataoperator.get(self.__plan, "Plan")
        modifier = 1 + plan_obj.commission
        if dataoperator.get(self.owner, "Client").precarious:
            modifier += plan_obj.increased_commission
        self.money *= modifier # ** (timekeeper.get() - self.__freeze_date)

    def get_offer(self, amount: float) -> bool:
        if amount > 0 and self.money >= amount and self.__freeze_date >= timekeeper.get():
            # self.__money -= amount
            return True
        return False

class CreditAccount(Account):
    __plan: int

    def __init__(self, owner: int, plan: int):
        super().__init__(owner)
        self.__plan = plan
        # self.__id = dataoperator.put(self)

    @property
    def plan(self):
        return self.__plan

    def update(self):
        if self.money >= 0:
            pass
        plan_obj = dataoperator.get(self.__plan, "Plan")
        modifier = 1 + plan_obj.commission
        if dataoperator.get(self.owner, "Client").precarious:
            modifier += plan_obj.increased_commission
        self.money *= modifier

    def get_offer(self, amount: float) -> bool:
        plan_obj = dataoperator.get(self.__plan, "Plan")
        if self.money - amount < plan_obj.limit:
            return False
        # self.__money -= amount
        return True
