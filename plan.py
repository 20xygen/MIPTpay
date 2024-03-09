import dataoperator
from dataoperator import put, get

class Plan:
    __id: int # PK
    __commission: float
    __increased_commission: float

    def __init__(self, commission: float, penalty: float = 0):
        self.__commission = commission
        self.__increased_commission = penalty
        self.__id = dataoperator.put(self)

    # def set_id(self, id: int):
    #     self.__id = id

    @property
    def commission(self):
        return self.__commission

    @property
    def penalty(self):
        return self.__increased_commission

    @property
    def id(self):
        return self.__id

class DepositPlan(Plan):
    __period: int

    def __init__(self, period: int, commission: float, penalty: float = 0):
        super().__init__(commission, penalty)
        self.__period = period

class CreditPlan(Plan):
    __limit: int
    __decreased_limit: int

    def __init__(self, limit: int, decreased_limit: int, commission: float, penalty: float = 0):
        super().__init__(commission, penalty)
        self.__limit = limit
        self.__decreased_limit = decreased_limit


