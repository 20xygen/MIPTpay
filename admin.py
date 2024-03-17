class Admin():
  """Admin - агрегатор структурных классов проекта. Дает доступ к исчерпывающей информации об объектах."""
  def info(self, object):
    print(1)
    real_names = [system_name.split("__")[1] for system_name in object.__dict__.keys()]
    s = []
    for real_name in real_names:
      try:
        val = str(getattr(object, real_name)())
        s.append(f"{real_name}: {val}")
      except:
        continue
    return '\n'.join(s)
  def account_info(self, account):
    from account import Account
    from dataoperator import DataOperator
    account = DataOperator().get(account, "Account")
    result = ""
    result += f"id: {account.id}\n"
    result += f"owner: {account.owner}\n"
    result += f"opened: {account.opened}\n"
    result += f"money: {account.money}\n"
    result += f"transfer: {account.transfer}\n"
    result += f"plan: {account.plan}\n"
    return result

  def bank_info(self, bank):
    from bank import Bank
    from dataoperator import DataOperator
    bank = DataOperator().get(bank, "Bank")
    result = ""
    result += f"id: {bank.id}\n"
    result += f"name: {bank.name}\n"
    result += f"clients: {bank.clients}\n"
    result += f"accounts: {bank.accounts}\n"
    result += f"plans: {bank.plans}\n"
    return result

  def client_info(self, client):
    from client import Client
    from dataoperator import DataOperator
    client = DataOperator().get(client, "Client")
    result = ""
    result += f"id: {client.id}\n"
    result += f"name: {client.name}\n"
    result += f"surname: {client.surname}\n"
    result += f"address: {client.address}\n"
    result += f"passport: {client.passport}\n"
    result += f"precarious: {client.precarious}\n"
    return result

  def person_info(self, person):
    from person import Person
    from dataoperator import DataOperator
    person = DataOperator().get(person, "Person")
    result = ""
    result += f"id: {person.id}\n"
    result += f"login: {person.login}\n"
    result += f"password: {person.password}\n"
    result += f"name: {person.name}\n"
    result += f"surname: {person.surname}\n"
    result += f"address: {person.address}\n"
    result += f"passport: {person.passport}\n"
    result += f"banks: {person.banks}\n"
    result += f"accounts: {person.accounts}\n"
    result += f"plans: {person.plans}\n"
    return result

  def plan_info(self, plan):
    from plan import Plan
    from dataoperator import DataOperator
    plan = DataOperator().get(plan, "Plan")
    result = ""
    result += f"id: {plan.id}\n"
    result += f"transfer_limit: {plan.transfer_limit}\n"
    result += f"decreased_transfer_limit: {plan.decreased_transfer_limit}\n"
    return result

  def transaction_info(self, transaction):
    from transaction import Transaction
    from dataoperator import DataOperator
    transaction = DataOperator().get(transaction, "Transaction")
    result = ""
    result += f"id: {transaction.id}\n"
    result += f"departure: {transaction.departure}\n"
    result += f"destination: {transaction.destination}\n"
    result += f"amount: {transaction.amount}\n"
    result += f"status: {transaction.status}\n"
    return result

  def revert_transaction(self, transaction: int) -> bool:
    # TODO: implement
    pass


