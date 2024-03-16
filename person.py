from typing import Dict

import dataoperator
from account import Account
from client import Client


class Person:
    '''Person - живой человек. Он может регистрироваться в банках и заводить счета.'''
    # TODO: Логины, пароли и тд
    __id: int  # PK
    __login: str
    __password: str
    __name: str
    __surname: str
    __address: str
    __passport: int
    __banks: Dict[str, int]
    __accounts: Dict[str, int]

    def __init__(self, login: str, password: str, name: str, surname: str, address: str = None, passport: int = None):
        import dataoperator
        self.__login = login
        self.__password = password
        self.__name = name
        self.__surname = surname
        self.__address = address
        self.__passport = passport
        self.__id = dataoperator.DataOperator().put(self)
        self.__banks = {}

    def login(self, login: str, password: str):
        # TODO: Сделать систему проверки пользователя
        pass

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

    @property
    def accounts(self):
        return self.__accounts

    @property
    def banks(self):
        return self.__banks

    def update(self, address: str, passport: int):
        self.__address = address
        self.__passport = passport
