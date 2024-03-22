import dataoperator


class Transaction:
    """ Any monetary transaction occurs with the creation of a transaction
    (so admins can track and/or cancel them). """

    __id: int
    __departure: int
    __destination: int
    __amount: float
    __status: int  # 0 - in progress, 1 - approved, -1 - cancelled

    def __init__(self, departure: int, destination: int, amount: float):
        self.__departure = departure
        self.__destination = destination
        self.__amount = amount
        self.__status = 0
        from dataoperator import DataOperator
        self.__id = DataOperator().put(self)

    @property
    def id(self):
        return self.__id

    def prove(self):
        self.__status = 1

    def cancel(self):
        self.__status = -1