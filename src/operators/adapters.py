import src
from datetime import datetime
#from dateutil import parser


class Adapter:
    def create_bank(self, bank: src.Bank):
        model = src.BankModel(name=bank.name)
        model.save()
        return model

    def create_person(self, person: src.Person):
        model = src.PersonModel(username=person.login, password=person.password, first_name=person.name, last_name=person.surname, email=person.address, passport=int(person.passport.replace(" ", "")))
        model.save()
        return model

    def create_client(self, client: src.Client, bank: src.BankModel, person: src.PersonModel):
        # print(bank.name)
        model = src.ClientModel(bank=bank, person=person, name=client.name, surname=client.surname, address=(client.address if client.address is not None else ""), passport=(int(client.passport) if client.passport is not None else 0), precarious=client.precarious)
        model.save()
        return model

    def create_plan(self, plan: src.Plan, bank: src.BankModel, name: str):
        model = src.PlanModel(name=name, bank=bank, commission=0, increased_commission=0, period=0, decreased_period=0, lower_limit=0, decreased_lower_limit=0, upper_limit=0, decreased_upper_limit=0, transfer_limit=0, decreased_transfer_limit=0)
        category: src.PlanCategoryModel
        if isinstance(plan, src.DebitPlan):
            category = src.PlanCategoryModel.objects.get(name='Debit')
            model.category = category
        elif isinstance(plan, src.DepositPlan):
            category = src.PlanCategoryModel.objects.get(name='Deposit')
            model.category = category
        elif isinstance(plan, src.CreditPlan):
            category = src.PlanCategoryModel.objects.get(name='Credit')
            model.category = category
        if category.commission:
            model.commission = plan.commission
            model.increased_commission = plan.increased_commission
        if category.period:
            model.period = plan.period
            model.decreased_period = plan.decreased_period
        if category.lower_limit:
            model.lower_limit = plan.lower_limit
            model.decreased_lower_limit = plan.decreased_lower_limit
        if category.upper_limit:
            model.upper_limit = plan.upper_limit
            model.decreased_lower_limit = plan.decreased_lower_limit
        if category.transfer_limit:
            model.transfer_limit = plan.transfer_limit
            model.decreased_transfer_limit = plan.decreased_transfer_limit
        model.save()
        return model

    def create_account(self, account: src.Account, bank: src.BankModel, client: src.ClientModel, plan: src.PlanModel):
        model = src.AccountModel(bank=bank, owner=client, opened=account.opened, money=account.money, transfer=account.transfer, plan=plan)
        if isinstance(account, src.DepositAccount):
            model.freeze_date = account.freeze_date
        else:
            model.freeze_date = 0
        model.save()
        return model

    def create_transaction(self, transaction: src.Transaction, dep: src.AccountModel, dest: src.AccountModel):
        model = src.TransactionModel(departure=dep, destination=dest, amount=transaction.amount, status=transaction.status)
        model.save()
        return model

    def set_date(self):
        model, created = src.DiaryModel.objects.get_or_create(parameter="Date")
        model.value = str(datetime.now())
        model.save()
        return model

    # def get_date_diff(self):  # -> datetime.timedelta
    #     raw = parser.parse(str(src.DiaryModel.objects.get(name='Date').value))
    #     date = datetime(raw.year, raw.month, raw.day, raw.hour, raw.minute, raw.second)
    #     diff = datetime.now() - date
    #     return diff

    def get_bank(self, ident: int) -> src.Bank:
        model = src.BankModel.objects.get(id=ident)
        clients = [it.id for it in src.ClientModel.objects.filter(bank=model)]
        accounts = [it.id for it in src.AccountModel.objects.filter(bank=model)]
        plans = [it.id for it in src.PlanModel.objects.filter(bank=model)]
        return src.Bank(model.id, model.name, clients, accounts, plans)

    def get_plan(self, ident: int) -> src.Plan:
        model = src.PlanModel.objects.get(id=ident)
        category = model.category
        if category.name == "Debit":
            return src.DebitPlan(ident, model.transfer_limit, model.decreased_transfer_limit)
        elif category.name == "Deposit":
            return src.DepositPlan(model.id, model.period, model.decreased_period, model.commission, model.increased_commission, model.transfer_limit, model.decreased_transfer_limit)
        elif category.name == "Credit":
            return src.CreditPlan(model.id, model.lower_limit, model.decreased_lower_limit, model.commission, model.increased_commission, model.transfer_limit, model.decreased_transfer_limit)

    def get_client(self, ident: int) -> src.Client:
        model = src.ClientModel.objects.get(id=ident)
        return src.Client(model.id, model.name, model.surname, model.address, str(model.password), model.precarious)

    def get_account(self, ident: int) -> src.Account:
        model = src.AccountModel.objects.get(id=ident)
        if model.plan.category.name == "Debit":
            return src.DebitAccount(model.id, model.owner.id, model.opened, model.money, model.transfer, model.plan.id)
        elif model.plan.category.name == "Deposit":
            return src.DepositAccount(model.id, model.owner.id, model.opened, model.money, model.transfer, model.plan.id, model.freeze_date)
        elif model.plan.category.name == "Credit":
            return src.CreditAccount(model.id, model.owner.id, model.opened, model.money, model.transfer, model.plan.id)

    def get_transaction(self, ident: int):
        model = src.TransactionModel.objects.get(id=ident)
        return src.Transaction(model.id, model.departure.id, model.destinations.id, model.amount, model.status)

    def create_person(self, ident: int):
        model = src.PersonModel.objects.get(id=ident)
        clients = [it.id for it in src.ClientModel.objects.filter(person=model)]
        return src.Person(model.id, model.login, model.password, model.name, model.surname, model.address, model.passport, clients)
