import src


class Message:
    __id: int
    __conversation: int
    __sender: int
    __text: str
    __status: bool


    def __init__(self, ident: int = None, conversation: int = None, sender: int = None, text: str = '', status: bool = None):
        self.__conversation = conversation
        self.__sender = sender
        self.__messages = []
        self.__text = text
        if ident is not None:
            self.__id = ident
            self.__status = status
        else:
            self.__status = True
            self.__id = src.SingleDO.DO().put(self, False)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, ident: int):
        self.__id = ident

    @property
    def conversation(self):
        return self.__conversation

    @conversation.setter
    def conversation(self, conversation: int):
        self.__conversation = conversation

    @property
    def sender(self):
        return self.__sender

    @sender.setter
    def sender(self, sender: int):
        self.__sender = sender

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: bool):
        self.__status = status
