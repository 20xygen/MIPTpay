import dataoperator
import timekeeper
from plan import DebitPlan, DepositPlan, CreditPlan


class Account:
    '''Банковский счет, привязан к клиенту банка.
    Через него происходят основные манипуляции на нижнем уровне.'''

    __id: int # PK
    __owner: int
    __opened: bool  # todo: action blocking decorator
    __money: float
    __transfer: float

    def __init__(self, owner):
        self.__owner = owner
        self.__opened = True
        self.__money = 0
        self.__id = dataoperator.put(self)
        self.__transfer = 0
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
    def transfer(self):
        return self.__transfer

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
    '''Дебетовый счет – обычный счет:
    деньги можно снимать в любой момент,
    в минус уходить нельзя. Комиссий нет.'''

    __plan: int

    @property
    def plan(self):
        return self.__plan

    def __init__(self, owner: int, plan: int):
        super().__init__(owner)
        self.__plan = plan

    def put_offer(self, amount: float) -> bool:
        plan_obj = dataoperator.get(self.plan, "Plan")
        lim = plan_obj.transfer_limit if not dataoperator.get(self.owner, "Client").precarious else plan_obj.decreased_transfer_limit
        if amount > 0 and self.transfer + amount <= lim:
            return True
        return False

    def get_offer(self, amount: float) -> bool:
        plan_obj = dataoperator.get(self.plan, "Plan")
        lim = plan_obj.transfer_limit if not dataoperator.get(self.owner, "Client").precarious else plan_obj.decreased_transfer_limit
        if 0 < amount <= self.money and self.transfer + amount <= lim:
            return True
        return False


class DepositAccount(Account):
    '''Депозит – счет, с ĸоторого нельзя снимать
    и переводить деньги до тех пор,
    поĸа не заĸончится его сроĸ (пополнять можно).'''
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

    def put_offer(self, amount: float) -> bool:
        plan_obj = dataoperator.get(self.plan, "Plan")
        lim = plan_obj.transfer_limit if not dataoperator.get(self.owner, "Client").precarious else plan_obj.decreased_transfer_limit
        if amount > 0 and self.transfer + amount <= lim:
            return True
        return False

    def get_offer(self, amount: float) -> bool:
        plan_obj = dataoperator.get(self.plan, "Plan")
        lim = plan_obj.transfer_limit if not dataoperator.get(self.owner, "Client").precarious else plan_obj.decreased_transfer_limit
        per = plan_obj.period if not dataoperator.get(self.owner, "Client").precarious else plan_obj.decreased_period
        if 0 < amount <= self.money and self.__freeze_date >= timekeeper.get() + per and self.transfer + amount <= lim:
            return True
        return False

class CreditAccount(Account):
    '''Кредитный счет – имеет ĸредитный лимит,
    в рамĸах ĸоторого можно уходить в минус (в плюс тоже можно).
    Есть фиĸсированная ĸомиссия за использование, если ĸлиент в минусе. '''

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
        tra = plan_obj.transfer_limit if not dataoperator.get(self.owner, "Client").precarious else plan_obj.decreased_transfer_limit
        lim = plan_obj.lower_limit if not dataoperator.get(self.owner, "Client").precarious else plan_obj.decreased_lower_limit
        if self.money - amount >= lim and amount > 0 and self.transfer + amount <= tra:
            return True
        return True

    def put_offer(self, amount: float) -> bool:
        plan_obj = dataoperator.get(self.plan, "Plan")
        lim = plan_obj.transfer_limit if not dataoperator.get(self.owner, "Client").precarious else plan_obj.decreased_transfer_limit
        if amount > 0 and self.transfer + amount <= lim:
            return True
        return False
