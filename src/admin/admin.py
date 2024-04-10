import src
from typing import Optional


class Admin:
    """ Admin is an aggregator of the project's structural classes.
    Provides access to comprehensive information about the objects. """

    # def info(self, object):
    #   print(1)
    #   real_names = [system_name.split("__")[1] for system_name in object.__dict__.keys()]
    #   s = []
    #   for real_name in real_names:
    #     try:
    #       val = str(getattr(object, real_name)())
    #       s.append(f"{real_name}: {val}")
    #     except:
    #       continue
    #   return '\n'.join(s)

    def account_info(self, account):
        account = src.DataOperator().get(account, "Account")
        ret = f"""id: {account.id}
        owner: {account.owner}
        opened: {account.opened}
        money: {account.money}
        transfer: {account.transfer}
        plan: {account.plan}"""
        src.DataOperator().done_with(account.id, "Account")
        return ret

    def bank_info(self, bank):
        bank = src.DataOperator().get(bank, "Bank")
        ret = f"""id: {bank.id}
        name: {bank.name}
        clients: {bank.clients}
        accounts: {bank.accounts}
        plans: {bank.plans}"""
        src.DataOperator().done_with(bank.id, "Bank")
        return ret

    def client_info(self, client):
        client = src.DataOperator().get(client, "Client")
        ret = f"""id: {client.id}
        name: {client.name}
        surname: {client.surname}
        address: {client.address}
        passport: {client.passport}
        precarious: {client.precarious}"""
        src.DataOperator().done_with(client.id, "Client")
        return ret

    def person_info(self, person):
        person = src.DataOperator().get(person, "Person")
        ret = f"""id: {person.id}
        login: {person.log_in}
        password: {person.password}
        name: {person.name}
        surname: {person.surname}
        address: {person.address}
        passport: {person.passport}
        banks: {person.banks}
        accounts: {person.accounts}
        plans: {person.plans}"""
        src.DataOperator().done_with(person.id, "Person")
        return ret

    def plan_info(self, plan):
        plan = src.DataOperator().get(plan, "Plan")
        ret = f"""id: {plan.id}
        transfer_limit: {plan.transfer_limit}
        decreased_transfer_limit: {plan.decreased_transfer_limit}"""
        src.DataOperator().done_with(plan.id, "Plan")
        return ret

    def transaction_info(self, transaction):
        transaction = src.DataOperator().get(transaction, "Transaction")
        ret = f"""id: {transaction.id}
        departure: {transaction.departure}
        destination: {transaction.destination}
        amount: {transaction.amount}
        status: {transaction.status}"""
        src.DataOperator().done_with(transaction.id, "Transaction")
        return ret

    def revert_transaction(self, trans: int) -> bool:
        transaction = src.DataOperator().get(trans, "Transaction")
        if transaction is None:
            return False
        transaction.revert()
        flag = True
        if transaction.departure:
            departure = src.DataOperator().get(transaction.departure, "Account")
            flag = flag and departure.put_offer(transaction.amount)
            departure.transfer -= transaction.amount
            departure.money += transaction.amount
            src.DataOperator().done_with(transaction.departure, "Transaction")
        if transaction.destination:
            destination = src.DataOperator().get(transaction.destination, "Account")
            flag = flag and destination.get_offer(transaction.amount)
            destination.transfer -= transaction.amount
            destination.money -= transaction.amount
            src.DataOperator().done_with(transaction.destination, "Transaction")
        return flag


class SingleAdmin:
    """Singleton wrapper for Admin class"""
    __single: int = 0
    __admin: Optional[Admin] = None

    def __init__(self):
        pass

    def get(self) -> Admin:
        if SingleAdmin.__single == 0:
            SingleAdmin.__admin = Admin()
            SingleAdmin.__single = 1
        return SingleAdmin.__admin




