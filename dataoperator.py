from client import Client
from account import Account
from bank import Bank
from plan import Plan
from typing import List, Dict

clients: Dict[int, Client] = {}
clients_counter = 0
global clients, clients_counter

accounts: Dict[int, Account] = {}
accounts_counter = 0
global accounts, accounts_counter

banks: Dict[int, Bank] = {}
banks_counter = 0
global banks, banks_counter

plans: Dict[int, Plan] = {}
plans_counter = 0
global plans, plans_counter

def get(id: int, type):
    container: Dict
    if type == Client:
        container = clients
    elif type == Bank:
        container = banks
    elif type == Account:
        container = accounts
    elif type == Plan:
        container = plans
    else:
        return None
    if not id in container.keys():
        return None
    else:
        return container[id]

def put(obj) -> int:
    if isinstance(obj, Client):
        clients_counter += 1
        clients[clients_counter] = obj
        return clients_counter
    if isinstance(obj, Bank):
        banks_counter += 1
        banks[banks_counter] = obj
        return banks_counter
    if isinstance(obj, Account):
        accounts_counter += 1
        accounts[accounts_counter] = obj
        return accounts_counter
    if isinstance(obj, Plan):
        plans_counter += 1
        plans[plans_counter] = obj
        return plans_counter