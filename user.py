import dataoperator
from dataoperator import *

class User:
    __login: str
    __password: str
    __name: str
    __surname: str
    __address: str
    __passport: int

    def __init__(self):
        self.__login = ""
        self.__password = ""
        self.__name = ""
        self.__surname = ""
        self.__address = ""
        self.__passport = 0

    def register(self, login: str, password: str, name: str, surname: str, address: str, passport: int):
        self.__login = login
        self.__password = password
        self.__name = name
        self.__surname = surname
        self.__address = address
        self.__passport = passport
        dataoperator.put(self)

    def login(self, login:str, password:str):
        # TODO: Сделать систему проверки пользователя
        pass

