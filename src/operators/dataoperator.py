from typing import Dict, Union, List
import src


clients: Dict[int, List[Union[src.Client, int]]] = {}
clients_counter = 0

accounts: Dict[int, List[Union[src.Account, int]]] = {}
accounts_counter = 0

banks: Dict[int, List[Union[src.Bank, int]]] = {}
banks_counter = 0

plans: Dict[int, List[Union[src.Plan, int]]] = {}
plans_counter = 0

transactions: Dict[int, List[Union[src.Transaction, int]]] = {}
transactions_counter = 0

persons: Dict[int, List[Union[src.Person, int]]] = {}
persons_counter = 0


class DataOperator:
    """ The class of interaction of logic with the database.
    Stores (reserves) objects that are currently being used by the system. """

    def get(self, id: int, type: str) -> Union[src.Client, src.Bank, src.Account, src.Plan, src.Transaction, src.Person, None]:
        type_to_container = {
            "Client": clients,
            "Bank": banks,
            "Account": accounts,
            "Plan": plans,
            "Transaction": transactions,
            "Person": persons
        }
        container = type_to_container.get(type, {})
        if id not in container.keys():
            print(type, ": not found object with id", id)
            return None
        else:
            # TODO: load from DB
            container[id][1] += 1
            return container[id][0]

    def put(self, obj, done: bool = True) -> int:
        global clients, clients_counter
        global accounts, accounts_counter
        global banks, banks_counter
        global plans, plans_counter
        global transactions, transactions_counter
        global persons, persons_counter
        amount_in_use = 0 if done else 1
        if isinstance(obj, src.Client):
            clients_counter += 1
            clients[clients_counter] = [obj, amount_in_use]
            return clients_counter
        if isinstance(obj, src.Bank):
            banks_counter += 1
            banks[banks_counter] = [obj, amount_in_use]
            return banks_counter
        if isinstance(obj, src.Account):
            accounts_counter += 1
            accounts[accounts_counter] = [obj, amount_in_use]
            return accounts_counter
        if isinstance(obj, src.Plan):
            plans_counter += 1
            plans[plans_counter] = [obj, amount_in_use]
            return plans_counter
        if isinstance(obj, src.Transaction):
            transactions_counter += 1
            transactions[transactions_counter] = [obj, amount_in_use]
            return transactions_counter
        if isinstance(obj, src.Person):
            persons_counter += 1
            persons[persons_counter] = [obj, amount_in_use]
            return persons_counter

    def get_bank_by_name(self, name: str):
        for ident, bank in banks.items():
            if bank[0].name == name:
                return bank
        return None

    def get_client_by_name(self, name: str):
        for ident, client in clients.items():
            if client[0].name == name:
                return client


    def account_info(self) -> str:
        st = ""
        for id, account in accounts.items():
            st += account[0].info() + '\n'
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

    def done_with(self, id: int, type: str) -> bool:
        type_to_container = {
            "Client": clients,
            "Bank": banks,
            "Account": accounts,
            "Plan": plans,
            "Transaction": transactions,
            "Person": persons
        }
        container = type_to_container.get(type, {})
        if id not in container.keys():
            return False
        else:
            container[id][1] -= 1
            # TODO: save to DB
            return True

    def print_online(self):
        print("Online objects:\n")
        for ident, bank in banks.items():
            if bank[1] > 0:
                print('\t', "Bank", ident, bank[1], bank[0].name)
        for ident, plan in plans.items():
            if plan[1] > 0:
                print('\t', "Plan", ident, plan[1])
        for ident, client in clients.items():
            if client[1] > 0:
                print('\t', "Client", ident, client[1], client[0].name)
        for ident, account in accounts.items():
            if account[1] > 0:
                print('\t', "Account", ident, account[1])
        for ident, person in persons.items():
            if person[1] > 0:
                print('\t', "Person", ident, person[1], person[0].name)
        for ident, transaction in transactions.items():
            if transaction[1] > 0:
                print('\t', "Transaction", ident, transaction[1])
        print("\nOffline objects:\n")
        for ident, bank in banks.items():
            if bank[1] == 0:
                print('\t', "Bank", ident, bank[1], bank[0].name)
        for ident, plan in plans.items():
            if plan[1] == 0:
                print('\t', "Plan", ident, plan[1])
        for ident, client in clients.items():
            if client[1] == 0:
                print('\t', "Client", ident, client[1], client[0].name)
        for ident, account in accounts.items():
            if account[1] == 0:
                print('\t', "Account", ident, account[1])
        for ident, person in persons.items():
            if person[1] == 0:
                print('\t', "Person", ident, person[1], person[0].name)
        for ident, transaction in transactions.items():
            if transaction[1] == 0:
                print('\t', "Transaction", ident, transaction[1])
        print("\nWTF objects:\n")
        for ident, bank in banks.items():
            if bank[1] < 0:
                print('\t', "Bank", ident, bank[1], bank[0].name)
        for ident, plan in plans.items():
            if plan[1] < 0:
                print('\t', "Plan", ident, plan[1])
        for ident, client in clients.items():
            if client[1] < 0:
                print('\t', "Client", ident, client[1], client[0].name)
        for ident, account in accounts.items():
            if account[1] < 0:
                print('\t', "Account", ident, account[1])
        for ident, person in persons.items():
            if person[1] < 0:
                print('\t', "Person", ident, person[1], person[0].name)
        for ident, transaction in transactions.items():
            if transaction[1] < 0:
                print('\t', "Transaction", ident, transaction[1])
        print("\n")


class SingleDataOperator:
    """Singleton wrapper for DataOperator class"""
    __single: int = 0
    __dataoperator: Optional[DataOperator] = None

    def __init__(self):
        pass

    def get(self) -> DataOperator:
        if SingleDataOperator.__single == 0:
            SingleDataOperator.__dataoperator = DataOperator()
            SingleDataOperator.__single = 1
        return SingleDataOperator.__dataoperator

    @property
    def dataoperator(self) -> DataOperator:
        return self.get()
