from typing import Dict, List
import src


class Person:
    """ The personal account of a real users - the user of the application. """

    # TODO: logins, passwords, etc
    __id: int  # PK
    __login: str
    __password: str
    __name: str
    __surname: str
    __address: str
    __passport: str
    # __banks: Dict[str, int]
    # __accounts: Dict[str, int]
    # __plans: Dict[int, int]
    __clients: List[int]

    # def __init__(self, login: str, password: str, name: str, surname: str, address: str = None, passport: str = None):
    #     self.__login = login
    #     self.__password = password
    #     self.__name = name
    #     self.__surname = surname
    #     self.__address = address
    #     self.__passport = passport
    #     self.__id = src.DataOperator().put(self, True)
    #     self.__clients = []

    # def __init__(self, ident: int, login: str, password: str, name: str, surname: str, address: str, passport: str, clients: List[int]):
    #     self.__id = ident
    #     self.__login = login
    #     self.__password = password
    #     self.__name = name
    #     self.__surname = surname
    #     self.__address = address
    #     self.__passport = passport
    #     self.__clients = clients

    def __init__(self, ident: int = None, name: str = None, surname: str = None, address: str = None, passport: str = None, clients: List[int] = None):
        # self.__login = login
        # self.__password = password
        self.__name = name
        self.__surname = surname
        self.__address = address
        self.__passport = passport
        if ident is not None:
            self.__id = ident
            self.__clients = clients
        else:
            print(f"It is deprecated to construct person with no id ({ident}).")
            self.__clients = []
            self.__id = src.DataOperator().put(self, True)

    def log_in(self, login: str, password: str):
        # TODO: Сделать систему проверки пользователя
        pass

    # @property
    # def login(self):
    #     return self.__login
    #
    # @property
    # def password(self):
    #     return self.__password

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

    # @property
    # def accounts(self):
    #     return self.__accounts
    #
    # @property
    # def banks(self):
    #     return self.__banks
    #
    # @property
    # def plans(self):
    #     return self.__plans

    def update(self, address: str, passport: str):
        self.__address = address
        self.__passport = passport


