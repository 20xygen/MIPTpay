from inspect import currentframe as cf
from typing import Optional
import src

class Client:
    """ Personal account of the banking's client.
    One users can have many of them (one per banking). """

    __id: int # PK
    __name: str
    __surname: str
    __address: str
    __passport: str
    __precarious: bool

    def __init__(self, name: str, surname: str, address: Optional[str] = None, passport: Optional[str] = None):
        self.__name = name
        self.__surname = surname
        self.__address = address
        self.__passport = passport
        if passport is None or address is None:
            self.__precarious = True
        else:
            self.__precarious = False
        self.__id = src.DataOperator().put(self)

    @property
    def precarious(self):
        src.available_from(cf(), "Bank", "ClientBuilder", "Account")
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
        src.available_from(cf(), "Bank", "ClientBuilder", "Account")
        return self.__address

    @property
    def passport(self):
        src.available_from(cf(), "Bank", "ClientBuilder", "Account")
        return self.__passport

    @address.setter
    def address(self, address: str):
        src.available_from(cf(), "Bank", "ClientBuilder")
        self.__address = address

    @passport.setter
    def passport(self, passport: str):
        src.available_from(cf(), "Bank", "ClientBuilder")
        self.__passport = passport

    def update(self, address: str, passport: str):
        src.available_from(cf(), "Bank", "ClientBuilder")
        self.__address = address
        self.__passport = passport
        self.validate()

    def validate(self):
        if self.passport is None or self.address is None:
            self.__precarious = True
        else:
            self.__precarious = False

