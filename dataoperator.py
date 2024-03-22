from person import Person
from client import Client
from account import Account
from bank import Bank
from plan import Plan
from typing import Dict, Union
from transaction import Transaction

clients: Dict[int, Client] = {}
clients_counter = 0

accounts: Dict[int, Account] = {}
accounts_counter = 0

banks: Dict[int, Bank] = {}
banks_counter = 0

plans: Dict[int, Plan] = {}
plans_counter = 0

transactions: Dict[int, Transaction] = {}
transactions_counter = 0

persons: Dict[int, Person] = {}
persons_counter = 0


class DataOperator:
    """ The class of interaction of logic with the database.
    Stores (reserves) objects that are currently being used by the system. """

    def get(self, id: int, type: str) -> Union[Client, Bank, Account, Plan, Transaction, Person, None]:
        type_to_container = {
            "Client": clients,
            "Bank": banks,
            "Account": accounts,
            "Plan": plans,
            "Transactions": transactions,
            "Person": persons
        }
        container = type_to_container.get(type, {})
        if id not in container.keys():
            return None
        else:
            return container[id]

    def put(self, obj) -> int:
        global clients, clients_counter
        global accounts, accounts_counter
        global banks, banks_counter
        global plans, plans_counter
        global transactions, transactions_counter
        global persons, persons_counter
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
        if isinstance(obj, Transaction):
            transactions_counter += 1
            transactions[transactions_counter] = obj
            return transactions_counter
        if isinstance(obj, Person):
            persons_counter += 1
            persons[persons_counter] = obj
            return persons_counter

    def get_bank_by_name(self, name: str):
        for ident, bank in banks.items():
            if bank.name == name:
                return bank
        return None

    def get_client_by_name(self, name: str):
        for ident, client in clients.items():
            if client.name == name:
                return client


    def account_info(self) -> str:
        st = ""
        for id, account in accounts.items():
            st += account.info() + '\n'
        return st

    def banks(self):
        return banks

    def plans(self):
        return plans

    def clients(self):
        return clients

    def accounts(self):
        return accounts

    def transactions(self):
        return transactions
