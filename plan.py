from accesstools import available_from
from inspect import currentframe as cf

class Plan:
    '''Тариф счета. Информация о комиссиях и ограничениях.'''

    __id: int # PK

    def __init__(self):
        import dataoperator
        from dataoperator import DataOperator
        self.__id = DataOperator().put(self)

    @property
    def id(self):
        return self.__id

class DebitPlan(Plan):
    '''Дебетовый тариф.'''

    __transfer_limit: float
    __decreased_transfer_limit: float

    @property
    def transfer_limit(self):
        available_from(cf(), "Bank", "Account")
        return self.__transfer_limit

    @property
    def decreased_transfer_limit(self):
        available_from(cf(), "Bank", "Account")
        return self.__decreased_transfer_limit

    def __init__(self, transfer_limit: float, decreased_transfer_limit: float):
        super().__init__()
        self.__transfer_limit = transfer_limit
        self.__decreased_transfer_limit = decreased_transfer_limit


class DepositPlan(Plan):
    '''Депозитный тариф.'''

    __period: int
    __decreased_period: int
    __commission: float
    __increased_commission: float
    __transfer_limit: float
    __decreased_transfer_limit: float

    @property
    def transfer_limit(self):
        available_from(cf(), "Bank", "Account")
        return self.__transfer_limit

    @property
    def decreased_transfer_limit(self):
        available_from(cf(), "Bank", "Account")
        return self.__decreased_transfer_limit

    @property
    def period(self):
        available_from(cf(), "Bank", "Account")
        return self.__period

    @property
    def decreased_period(self):
        available_from(cf(), "Bank", "Account")
        return self.__decreased_period

    @property
    def commission(self):
        available_from(cf(), "Bank", "Account")
        return self.__commission

    @property
    def increased_commission(self):
        available_from(cf(), "Bank", "Account")
        return self.__increased_commission

    def __init__(self, period: int, decreased_period: int,
                 commission: float, increased_commission: float,
                 transfer_limit: float, decreased_transfer_limit: float):
        super().__init__()
        self.__period = period
        self.__decreased_period = decreased_period
        self.__commission = commission
        self.__increased_commission = increased_commission
        self.__transfer_limit = transfer_limit
        self.__decreased_transfer_limit = decreased_transfer_limit



class CreditPlan(Plan):
    '''Кредитный тариф.'''

    __lower_limit: float
    __decreased_lower_limit: float
    __commission: float
    __increased_commission: float
    __transfer_limit: float
    __decreased_transfer_limit: float

    @property
    def transfer_limit(self):
        available_from(cf(), "Bank", "Account")
        return self.__transfer_limit

    @property
    def decreased_transfer_limit(self):
        available_from(cf(), "Bank", "Account")
        return self.__decreased_transfer_limit

    @property
    def lower_limit(self):
        available_from(cf(), "Bank", "Account")
        return self.__lower_limit

    @property
    def decreased_lower_limit(self):
        available_from(cf(), "Bank", "Account")
        return self.__decreased_lower_limit

    @property
    def commission(self):
        available_from(cf(), "Bank", "Account")
        return self.__commission

    @property
    def increased_commission(self):
        available_from(cf(), "Bank", "Account")
        return self.__increased_commission

    def __init__(self, lower_limit: float, decreased_lower_limit: float,
                 commission: float, increased_commission: float,
                 transfer_limit: float, decreased_transfer_limit: float):
        super().__init__()
        self.__lower_limit = lower_limit
        self.__decreased_lower_limit = decreased_lower_limit
        self.__commission = commission
        self.__increased_commission = increased_commission
        self.__transfer_limit = transfer_limit
        self.__decreased_transfer_limit = decreased_transfer_limit


