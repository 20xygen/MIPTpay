from accesstools import available_from
from inspect import currentframe as cf

class Client:
    '''Личный кабинет клиента банка.
    У одного человека (Human) их может быть много
    (по одному на банк).'''

    __id: int # PK
    __name: str
    __surname: str
    __address: str
    __passport: int
    __precarious: bool

    def __init__(self, name: str, surname: str, address: str = None, passport: int = None):
        self.__name = name
        self.__surname = surname
        self.__address = address
        self.__passport = passport
        if passport is None or address is None:
            self.__precarious = True
        else:
            self.__precarious = False
        from dataoperator import DataOperator
        self.__id = DataOperator().put(self)

    @property
    def precarious(self):
        available_from(cf(), "Bank", "ClientBuilder", "Account")
        return self.__precarious

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def surname(self):
        return self.__surname

    @property
    def address(self):
        available_from(cf(), "Bank", "ClientBuilder", "Account")
        return self.__address

    @property
    def passport(self):
        available_from(cf(), "Bank", "ClientBuilder", "Account")
        return self.__passport

    @address.setter
    def address(self, address: str):
        available_from(cf(), "Bank", "ClientBuilder")
        self.__address = address

    @passport.setter
    def passport(self, passport: int):
        available_from(cf(), "Bank", "ClientBuilder")
        self.__passport = passport

    def update(self, address: str, passport: int):
        available_from(cf(), "Bank", "ClientBuilder")
        self.__address = address
        self.__passport = passport
        self.validate()

    def validate(self):
        if self.passport is None or self.address is None:
            self.__precarious = True
        else:
            self.__precarious = False

