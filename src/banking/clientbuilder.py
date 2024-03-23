from typing import Optional
import src


class ClientBuilder:
    """ Builder class for creating Client instances. """

    __brick: Optional[src.Client]

    def reset(self, name: str, surname: str):
        self.__brick = src.Client(name, surname)

    def address(self, address: str):
        self.__brick.address = address

    def passport(self, passport: str):
        self.__brick.passport = passport

    def get(self) -> src.Client:
        brick = self.__brick
        brick.validate()
        self.__brick = None
        return brick