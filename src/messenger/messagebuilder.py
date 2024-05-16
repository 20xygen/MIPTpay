import src
from typing import Optional


class MessageBuilder:
    __obj: Optional[src.Message]

    def reset(self, conversation: int, sender: int):
        self.__obj = src.Message(None, conversation, sender)

    def fill(self, text: str):
        self.__obj.text = text

    def get(self):
        buff = self.__obj
        self.__obj = None
        return buff


class SingleMB:
    """Singleton wrapper for MessageBuilder class"""
    __builder: Optional[MessageBuilder] = None

    def __init__(self):
        pass

    @classmethod
    def MB(cls) -> MessageBuilder:
        if SingleMB.__builder is None:
            SingleMB.__builder = MessageBuilder()
        return SingleMB.__builder