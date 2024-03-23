import src


class Admin():
  """ Admin is an aggregator of the project's structural classes.
  Provides access to comprehensive information about the objects. """

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
    account = src.DataOperator().get(account, "Account")
    return f"""id: {account.id}
    owner: {account.owner}
    opened: {account.opened}
    money: {account.money}
    transfer: {account.transfer}
    plan: {account.plan}"""


  def bank_info(self, bank):
    bank = src.DataOperator().get(bank, "Bank")
    return f"""id: {bank.id}
    name: {bank.name}
    clients: {bank.clients}
    accounts: {bank.accounts}
    plans: {bank.plans}"""

  def client_info(self, client):
    client = src.DataOperator().get(client, "Client")
    return f"""id: {client.id}
    name: {client.name}
    surname: {client.surname}
    address: {client.address}
    passport: {client.passport}
    precarious: {client.precarious}"""

  def person_info(self, person):
    person = src.DataOperator().get(person, "Person")
    return f"""id: {person.id}
    login: {person.login}
    password: {person.password}
    name: {person.name}
    surname: {person.surname}
    address: {person.address}
    passport: {person.passport}
    banks: {person.banks}
    accounts: {person.accounts}
    plans: {person.plans}"""

  def plan_info(self, plan):
    plan = src.DataOperator().get(plan, "Plan")
    return f"""id: {plan.id}
    transfer_limit: {plan.transfer_limit}
    decreased_transfer_limit: {plan.decreased_transfer_limit}"""

  def transaction_info(self, transaction):
    transaction = src.DataOperator().get(transaction, "Transaction")
    return f"""id: {transaction.id}
    departure: {transaction.departure}
    destination: {transaction.destination}
    amount: {transaction.amount}
    status: {transaction.status}"""

  def revert_transaction(self, transaction: int) -> bool:
    transaction = src.DataOperator.get(transaction, "Transaction")
    transaction.cancel()
    departure = src.DataOperator.get(transaction._Transaction__departure, "Account")
    destination = src.DataOperator.get(transaction._Transaction__destination, "Account")
    if destination.money >= transaction.amount():
      departure.money += transaction.amount()
      destination.money -= transaction.amount()
      return "Success"
    else:
      return "Unable to revert transaction: Insufficient funds"


