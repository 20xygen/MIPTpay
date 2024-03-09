from typing import List
from account import Account

class Client:
    __id: int # PK
    __name: str
    __surname: str
    __address: str
    __passport: int
    __precarious: bool
    __accounts: List[Account]

    def __init__(self, name: str, surname: str, address: str = None, passport: int = None):
        self.__name = name
        self.__surname = surname
        self.__address = address
        self.__passport = passport
        if passport is None or address is None:
            self.__precarious = True
        else:
            self.__precarious = False

    def is_precarious(self):
        return self.__precarious
