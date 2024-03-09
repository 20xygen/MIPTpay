import dataoperator


class Transaction:
    __id: int
    __departure: int
    __destination: int
    __amount: int
    __status: int # 0 - in progress, 1 - approved, -1 - cancelled

    def __init__(self, departure: int, destination: int, amount: int):
        self.__departure = departure
        self.__destination = destination
        self.__amount = amount
        self.__status = 0
        self.__id = dataoperator.put(self)

    @property
    def id(self):
        return self.__id

    def prove(self):
        self.__status = 1

    def cancel(self):
        self.__status = -1