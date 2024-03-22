from accesstools import available_from
from inspect import currentframe as cf


class Account:
    """ A bank account linked to a bank customer.
    Through it, the main manipulations take place at the lower level. """

    __id: int # PK
    __owner: int
    __opened: bool  # TODO: action blocking decorator
    __money: float
    __transfer: float

    def __init__(self, owner):
        self.__owner = owner
        self.__opened = True
        self.__money = 0
        from dataoperator import DataOperator
        self.__id = DataOperator().put(self)
        self.__transfer = 0
        from timekeeper import TimeKeeper
        TimeKeeper().add(self.__id)

    def put(self, cash: float) -> int:
        available_from(cf(), "Bank")
        self.__money += cash
        return self.__id

    def get(self, cash: float) -> int:
        available_from(cf(), "Bank")
        self.__money -= cash
        return self.__id

    @property
    def id(self):
        return self.__id

    @property
    def owner(self):
        available_from(cf(), "Bank")
        return self.__owner

    @property
    def transfer(self):
        available_from(cf(), "Bank")
        return self.__transfer

    @property
    def opened(self):
        available_from(cf(), "Bank")
        return self.__opened

    @property
    def money(self):
        available_from(cf(), "Bank")
        return self.__money

    @money.setter
    def money(self, money):
        available_from(cf(), "Bank")
        self.__money = money

    @property
    def owner(self):
        available_from(cf(), "Bank")
        return self.__owner

    def put_offer(self, cash: float) -> bool:
        available_from(cf(), "Bank")
        if cash < 0:
            return False
        # self.__money += cash
        return True

    def get_offer(self, amount: float) -> bool:
        available_from(cf(), "Bank")
        if amount > 0 and self.__money >= amount:
            return True
        return False

    def update(self):
        available_from(cf(), "TimeKeeper")
        pass

    def info(self) -> str:
        available_from(cf(), "Bank", "DataOperator")
        st = str(self.id) + ("(open)" if self.opened else "(closed)") + '\n'
        from dataoperator import DataOperator
        owner_obj = DataOperator().get(self.owner, "Client")
        if owner_obj is None:
            "Error in account::info()"
        st += f"Owner: {owner_obj.name} {owner_obj.surname}\n"
        st += ("Precarious" if owner_obj.precarious else "Not precarious") + f": {owner_obj.address} {owner_obj.passport}\n"
        st += str(self.money) + "\n"
        return st

class DebitAccount(Account):
    """ Debit account – a regular account: money can be withdrawn at any time,
    you can not go into the negative. There are no commissions. """

    __plan: int

    @property
    def plan(self):
        return self.__plan

    def __init__(self, owner: int, plan: int):
        super().__init__(owner)
        self.__plan = plan

    def put_offer(self, amount: float) -> bool:
        available_from(cf(), "Bank")
        from dataoperator import DataOperator
        plan_obj = DataOperator().get(self.plan, "Plan")
        client_obj = DataOperator().get(self.owner, "Client")
        if plan_obj is None or client_obj is None:
            return False
        lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
        if amount > 0 and self.transfer + amount <= lim:
            return True
        return False

    def get_offer(self, amount: float) -> bool:
        available_from(cf(), "Bank")
        from dataoperator import DataOperator
        plan_obj = DataOperator().get(self.plan, "Plan")
        client_obj = DataOperator().get(self.owner, "Client")
        if plan_obj is None or client_obj is None:
            return False
        lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
        if 0 < amount <= self.money and self.transfer + amount <= lim:
            return True
        return False


class DepositAccount(Account):
    """ A deposit is an account that cannot be withdrawn from
    and transfer the money until its term ends (you can replenish it). """

    __plan: int
    __freeze_date: int

    @property
    def plan(self):
        available_from(cf(), "Bank")
        return self.__plan

    @property
    def freeze_date(self):
        available_from(cf(), "Bank")
        return self.__freeze_date

    def __init__(self, owner: int, plan: int):
        super().__init__(owner)
        self.__plan = plan
        from dataoperator import DataOperator
        plan_obj = DataOperator().get(plan, "Plan")
        from timekeeper import TimeKeeper
        self.__freeze_date = TimeKeeper().get()

    def update(self):
        available_from(cf(), "TimeKeeper")
        from dataoperator import DataOperator
        plan_obj = DataOperator().get(self.__plan, "Plan")
        modifier = 1 + plan_obj.commission
        client_obj = DataOperator().get(self.owner, "Client")
        if client_obj is None:
            return False
        if client_obj.precarious:
            modifier += plan_obj.increased_commission
        self.money *= modifier

    def put_offer(self, amount: float) -> bool:
        available_from(cf(), "Bank")
        from dataoperator import DataOperator
        plan_obj = DataOperator().get(self.plan, "Plan")
        client_obj = DataOperator().get(self.owner, "Client")
        if plan_obj is None or client_obj is None:
            return False
        lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
        if amount > 0 and self.transfer + amount <= lim:
            return True
        return False

    def get_offer(self, amount: float) -> bool:
        available_from(cf(), "Bank")
        from dataoperator import DataOperator
        from timekeeper import TimeKeeper
        plan_obj = DataOperator().get(self.plan, "Plan")
        client_obj = DataOperator().get(self.owner, "Client")
        if plan_obj is None or client_obj is None:
            return False
        lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
        per = plan_obj.period if not DataOperator().get(self.owner, "Client").precarious else plan_obj.decreased_period
        if 0 < amount <= self.money and self.__freeze_date >= TimeKeeper().get() + per and self.transfer + amount <= lim:
            return True
        return False

class CreditAccount(Account):
    """ A credit account has a credit limit, within
    the limits of which you can go into the negative (you can also go into the plus).
    There is a fee for use if the customer is in the red. """

    __plan: int

    def __init__(self, owner: int, plan: int):
        super().__init__(owner)
        self.__plan = plan

    @property
    def plan(self):
        available_from(cf(), "Bank")
        return self.__plan

    def update(self):
        available_from(cf(), "Bank", "TimeKeeper")
        if self.money >= 0:
            pass
        from dataoperator import DataOperator
        plan_obj = DataOperator().get(self.__plan, "Plan")
        client_obj = DataOperator().get(self.owner, "Client")
        if plan_obj is None or client_obj is None:
            return False
        modifier = 1 + plan_obj.commission
        if client_obj.precarious:
            modifier += plan_obj.increased_commission
        self.money *= modifier

    def get_offer(self, amount: float) -> bool:
        available_from(cf(), "Bank")
        from dataoperator import DataOperator
        plan_obj = DataOperator().get(self.__plan, "Plan")
        client_obj = DataOperator().get(self.owner, "Client")
        if plan_obj is None or client_obj is None:
            return False
        tra = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
        lim = plan_obj.lower_limit if not client_obj.precarious else plan_obj.decreased_lower_limit
        if self.money - amount >= lim and amount > 0 and self.transfer + amount <= tra:
            return True
        return True

    def put_offer(self, amount: float) -> bool:
        available_from(cf(), "Bank")
        from dataoperator import DataOperator
        plan_obj = DataOperator().get(self.plan, "Plan")
        client_obj = DataOperator().get(self.owner, "Client")
        if plan_obj is None or client_obj is None:
            return False
        lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
        if amount > 0 and self.transfer + amount <= lim:
            return True
        return False
