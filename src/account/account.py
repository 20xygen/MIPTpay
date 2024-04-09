from inspect import currentframe as cf
import src


class Account:
    """ A banking account linked to a banking customer.
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
        self.__transfer = 0
        self.__id = src.DataOperator().put(self, False)
        src.TimeKeeper().add(self.__id)

    def __init__(self):
        pass

    def put(self, cash: float) -> int:
        src.available_from(cf(), "Bank")
        self.__money += cash
        return self.__id

    def get(self, cash: float) -> int:
        src.available_from(cf(), "Bank")
        self.__money -= cash
        return self.__id

    @property
    def id(self):
        return self.__id

    @property
    def owner(self):
        src.available_from(cf(), "Bank")
        return self.__owner

    @property
    def transfer(self):
        src.available_from(cf(), "Bank")
        return self.__transfer

    @transfer.setter
    def transfer(self, cash: float):
        src.available_from(cf(), "Bank")
        self.__transfer = cash

    @property
    def opened(self):
        src.available_from(cf(), "Bank")
        return self.__opened

    @property
    def money(self):
        src.available_from(cf(), "Bank")
        return self.__money

    @money.setter
    def money(self, money):
        src.available_from(cf(), "Bank")
        self.__money = money

    def put_offer(self, cash: float) -> bool:
        src.available_from(cf(), "Bank")
        if cash < 0:
            return False
        # self.__money += cash
        return True

    def get_offer(self, amount: float) -> bool:
        src.available_from(cf(), "Bank")
        if amount > 0 and self.__money >= amount:
            return True
        return False

    def update(self):
        src.available_from(cf(), "TimeKeeper")
        pass

    def info(self) -> str:
        src.available_from(cf(), "Bank", "DataOperator")
        st = str(self.id) + ("(open)" if self.opened else "(closed)")
        owner_obj = src.DataOperator().get(self.owner, "Client")
        ret = "Error in account::info()"
        if owner_obj is not None:
            ret = f"""{st}
            Owner: {owner_obj.name} {owner_obj.surname}
            {("Precarious" if owner_obj.precarious else "Not precarious") + f": {owner_obj.address} {owner_obj.passport}"}
            {str(self.money)}"""
        src.DataOperator().done_with(owner_obj.id, "Client")
        return ret

class DebitAccount(Account):
    """ Debit account – a regular account: money can be withdrawn at any time,
    you can not go into the negative. There are no commissions. """

    __plan: int

    def __init__(self, ident: int, owner: int, opened: bool, money: float, transfer: float, plan: int):
        src.available_from(cf())
        super()
        self.__id = ident
        self.__owner = owner
        self.__opened = opened
        self.__money = money
        self.__transfer = transfer
        self.__plan = plan

    @property
    def plan(self):
        return self.__plan

    def __init__(self, owner: int, plan: int):
        super().__init__(owner)
        self.__plan = plan
        src.DataOperator().done_with(self.id, "Account")

    def put_offer(self, amount: float) -> bool:
        src.available_from(cf(), "Bank")
        plan_obj = src.DataOperator().get(self.plan, "Plan")
        client_obj = src.DataOperator().get(self.owner, "Client")
        ret = False
        if plan_obj is not None and client_obj is not None:
            lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
            if amount > 0 and self.transfer + amount <= lim:
                ret = True
            else:
                ret = False
        src.DataOperator().done_with(self.plan, "Plan")
        src.DataOperator().done_with(self.owner, "Client")
        return ret

    def get_offer(self, amount: float) -> bool:
        src.available_from(cf(), "Bank")
        plan_obj = src.DataOperator().get(self.plan, "Plan")
        client_obj = src.DataOperator().get(self.owner, "Client")
        ret = False
        if plan_obj is not None and client_obj is not None:
            lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
            if 0 < amount <= self.money and self.transfer + amount <= lim:
                ret = True
            else:
                ret = False
        src.DataOperator().done_with(self.plan, "Plan")
        src.DataOperator().done_with(self.owner, "Client")
        return ret


class DepositAccount(Account):
    """ A deposit is an account that cannot be withdrawn from
    and transfer the money until its term ends (you can replenish it). """

    __plan: int
    __freeze_date: int

    def __init__(self, ident: int, owner: int, opened: bool, money: float, transfer: float, plan: int, freeze_date: int):
        src.available_from(cf())
        super()
        self.__id = ident
        self.__owner = owner
        self.__opened = opened
        self.__money = money
        self.__transfer = transfer
        self.__plan = plan
        self.__freeze_date = freeze_date

    @property
    def plan(self):
        src.available_from(cf(), "Bank")
        return self.__plan

    @property
    def freeze_date(self):
        src.available_from(cf(), "Bank")
        return self.__freeze_date

    def __init__(self, owner: int, plan: int):
        super().__init__(owner)
        self.__plan = plan
        self.__freeze_date = src.TimeKeeper().get()
        src.DataOperator().done_with(self.id, "Account")

    def update(self):
        src.available_from(cf(), "TimeKeeper")
        plan_obj = src.DataOperator().get(self.__plan, "Plan")
        modifier = 1 + plan_obj.commission
        client_obj = src.DataOperator().get(self.owner, "Client")
        if client_obj is None:
            src.DataOperator().done_with(self.plan, "Plan")
            src.DataOperator().done_with(self.owner, "Client")
            return
        if client_obj.precarious:
            modifier += plan_obj.increased_commission
        self.money *= modifier
        src.DataOperator().done_with(self.plan, "Plan")
        src.DataOperator().done_with(self.owner, "Client")

    def put_offer(self, amount: float) -> bool:
        src.available_from(cf(), "Bank")
        plan_obj = src.DataOperator().get(self.plan, "Plan")
        client_obj = src.DataOperator().get(self.owner, "Client")
        ret = False
        if plan_obj is not None and client_obj is not None:
            lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
            if amount > 0 and self.transfer + amount <= lim:
                ret = True
        src.DataOperator().done_with(self.plan, "Plan")
        src.DataOperator().done_with(self.owner, "Client")
        return ret

    def get_offer(self, amount: float) -> bool:
        src.available_from(cf(), "Bank")
        plan_obj = src.DataOperator().get(self.plan, "Plan")
        client_obj = src.DataOperator().get(self.owner, "Client")
        ret = False
        if plan_obj is not None and client_obj is not None:
            lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
            per = plan_obj.period if not src.DataOperator().get(self.owner, "Client").precarious else plan_obj.decreased_period
            if 0 < amount <= self.money and self.__freeze_date >= src.TimeKeeper().get() + per and self.transfer + amount <= lim:
                ret = True
        src.DataOperator().done_with(self.plan, "Plan")
        src.DataOperator().done_with(self.owner, "Client")
        return ret

class CreditAccount(Account):
    """ A credit account has a credit limit, within
    the limits of which you can go into the negative (you can also go into the plus).
    There is a fee for use if the customer is in the red. """

    __plan: int

    def __init__(self, ident: int, owner: int, opened: bool, money: float, transfer: float, plan: int):
        src.available_from(cf())
        super()
        self.__id = ident
        self.__owner = owner
        self.__opened = opened
        self.__money = money
        self.__transfer = transfer
        self.__plan = plan

    def __init__(self, owner: int, plan: int):
        super().__init__(owner)
        self.__plan = plan
        src.DataOperator().done_with(self.id, "Account")

    @property
    def plan(self):
        src.available_from(cf(), "Bank")
        return self.__plan

    def update(self):
        src.available_from(cf(), "Bank", "TimeKeeper")
        if self.money >= 0:
            pass
        
        plan_obj = src.DataOperator().get(self.__plan, "Plan")
        client_obj = src.DataOperator().get(self.owner, "Client")
        if plan_obj is None or client_obj is None:
            src.DataOperator().done_with(self.plan, "Plan")
            src.DataOperator().done_with(self.owner, "Client")
            return
        modifier = 1 + plan_obj.commission
        if client_obj.precarious:
            modifier += plan_obj.increased_commission
        self.money *= modifier
        src.DataOperator().done_with(self.plan, "Plan")
        src.DataOperator().done_with(self.owner, "Client")

    def get_offer(self, amount: float) -> bool:
        src.available_from(cf(), "Bank")
        plan_obj = src.DataOperator().get(self.__plan, "Plan")
        client_obj = src.DataOperator().get(self.owner, "Client")
        ret = False
        if plan_obj is not None and client_obj is not None:
            tra = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
            lim = plan_obj.lower_limit if not client_obj.precarious else plan_obj.decreased_lower_limit
            if self.money - amount >= lim and amount > 0 and self.transfer + amount <= tra:
                ret= True
        src.DataOperator().done_with(self.plan, "Plan")
        src.DataOperator().done_with(self.owner, "Client")
        return ret

    def put_offer(self, amount: float) -> bool:
        src.available_from(cf(), "Bank")
        plan_obj = src.DataOperator().get(self.plan, "Plan")
        client_obj = src.DataOperator().get(self.owner, "Client")
        ret = False
        if plan_obj is not None and client_obj is not None:
            lim = plan_obj.transfer_limit if not client_obj.precarious else plan_obj.decreased_transfer_limit
            if amount > 0 and self.transfer + amount <= lim:
                ret = True
        src.DataOperator().done_with(self.plan, "Plan")
        src.DataOperator().done_with(self.owner, "Client")
        return ret
