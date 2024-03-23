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
    result = ""
    result += f"id: {account.id}\n"
    result += f"owner: {account.owner}\n"
    result += f"opened: {account.opened}\n"
    result += f"money: {account.money}\n"
    result += f"transfer: {account.transfer}\n"
    result += f"plan: {account.plan}\n"
    return result

  def bank_info(self, bank):
    bank = src.DataOperator().get(bank, "Bank")
    result = ""
    result += f"id: {bank.id}\n"
    result += f"name: {bank.name}\n"
    result += f"clients: {bank.clients}\n"
    result += f"accounts: {bank.accounts}\n"
    result += f"plans: {bank.plans}\n"
    return result

  def client_info(self, client):
    client = src.DataOperator().get(client, "Client")
    result = ""
    result += f"id: {client.id}\n"
    result += f"name: {client.name}\n"
    result += f"surname: {client.surname}\n"
    result += f"address: {client.address}\n"
    result += f"passport: {client.passport}\n"
    result += f"precarious: {client.precarious}\n"
    return result

  def person_info(self, person):
    person = src.DataOperator().get(person, "Person")
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
    plan = src.DataOperator().get(plan, "Plan")
    result = ""
    result += f"id: {plan.id}\n"
    result += f"transfer_limit: {plan.transfer_limit}\n"
    result += f"decreased_transfer_limit: {plan.decreased_transfer_limit}\n"
    return result

  def transaction_info(self, transaction):
    transaction = src.DataOperator().get(transaction, "Transaction")
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


