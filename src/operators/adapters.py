import src
from datetime import datetime
from dateutil import parser


class Adapter:
    def create_bank(self, bank: src.Bank):
        model = src.BankModel(name=bank.name)
        model.save()
        return model

    def create_person(self, person: src.Person):
        model = src.PersonModel(login=person.log_in, password=person.password, name=person.name, surname=person.surname, address=person.address, passport=int(person.passport.replace(" ", "")))
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

    def get_date_diff(self):  # -> datetime.timedelta
        raw = parser.parse(str(src.DiaryModel.objects.get(name='Date').value))
        date = datetime(raw.year, raw.month, raw.day, raw.hour, raw.minute, raw.second)
        diff = datetime.now() - date
        return diff


