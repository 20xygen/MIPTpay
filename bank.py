from typing import Dict, List, Tuple
from client import Client
from account import Account

class Bank:
    __id: int # PK
    __name: str
    __clients: List[Client]
    __accounts: List[Account]

