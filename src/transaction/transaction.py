from inspect import currentframe as cf
import src


class Transaction:
    """ Any monetary transaction occurs with the creation of a transaction
    (so admins can track and/or cancel them). """

    __id: int
    __departure: int
    __destination: int
    __amount: float
    __status: int  # 0 - in progress, 1 - approved, -1 - cancelled, -2 - reverted

    def __init__(self, departure: int, destination: int, amount: float):
        self.__departure = departure
        self.__destination = destination
        self.__amount = amount
        self.__status = 0
        self.__id = src.DataOperator().put(self, False) # Transaction closes later

    def __init__(self, ident: int, departure: int, destination: int, amount: float, status: int):
        src.available_from(cf())
        self.__id = ident
        self.__departure = departure
        self.__destination = destination
        self.__amount = amount
        self.__status = status

    @property
    def id(self):
        return self.__id

    @property
    def amount(self):
        return self.__amount

    @property
    def status(self):
        return self.__status

    def prove(self):
        self.__status = 1

    def cancel(self):
        self.__status = -1

    def revert(self):
        self.__status = -2