from typing import Dict
from account import Account
from client import Client


class Person:
    '''Person - реальный человек. Он может регистрироваться в банках и заводить счета.'''

    __id: int # PK
    __name: str
    __surname: str
    __address: str
    __passport: int

    def __init__(self, name: str, surname: str, address: str = None, passport: int = None):
        import dataoperator
        self.__name = name
        self.__surname = surname
        self.__address = address
        self.__passport = passport
        self.__id = dataoperator.put(self)

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
        return self.__address

    @property
    def passport(self):
        return self.__passport

    def update(self, address: str, passport: int):
        self.__address = address
        self.__passport = passport








