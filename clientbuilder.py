from client import Client
from typing import Optional

class ClientBuilder:
    '''Bulder class for creating Client instances.'''

    __brick: Optional[Client]

    def reset(self, name: str, surname: str):
        self.__brick = Client(name, surname)

    def address(self, address: str):
        self.__brick.address = address

    def passport(self, passport: int):
        self.__brick.passport = passport

    def get(self) -> Client:
        brick = self.__brick
        brick.validate()
        self.__brick = None
        return brick