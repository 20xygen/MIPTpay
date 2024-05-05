import src
from typing import List


class Conversation:
    __id: int
    __senders: List[int]
    __status: bool
    __messages: List[int]


    def __init__(self, ident: int = None, senders: List[int] = None, messages: List[int] = None, status: bool = None):
        self.__senders = senders
        if ident is not None:
            self.__id = ident
            self.__messages = messages
            self.__status = status
        else:
            self.__status = True
            self.__messages = []
            self.__id = src.SingleDO.DO().put(self, True)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, ident: int):
        self.__id = ident

    @property
    def senders(self):
        return self.__senders

    @senders.setter
    def senders(self, senders: List[int]):
        self.__senders = senders

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: bool):
        self.__status = status

    @property
    def messages(self):
        return self.__messages

    @messages.setter
    def messages(self, messages: List[int]):
        self.__messages = messages

