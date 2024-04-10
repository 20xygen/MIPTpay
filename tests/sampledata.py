import src

src.DiaryModel.objects.all().delete()
src.BankModel.objects.all().delete()
src.PersonModel.objects.all().delete()
src.ClientModel.objects.all().delete()
src.PlanCategoryModel.objects.all().delete()
src.PlanModel.objects.all().delete()
src.AccountModel.objects.all().delete()
src.TransactionModel.objects.all().delete()


# Data

src.Adaptor().set_date()

# Plan categories

debit = src.PlanCategoryModel(name="Debit", commission=False, period=False, lower_limit=False, upper_limit=False, transfer_limit=True)
debit.save()
deposit = src.PlanCategoryModel(name="Deposit", commission=True, period=True, lower_limit=False, upper_limit=False, transfer_limit=True)
deposit.save()
credit = src.PlanCategoryModel(name="Credit", commission=True, period=False, lower_limit=True, upper_limit=False, transfer_limit=True)
credit.save()

# Banks

sber = src.Bank("Sberbank")
sber_model = src.Adaptor().create_bank(sber)

tink = src.Bank("Tinkoff")
tink_model = src.Adaptor().create_bank(tink)

# Plans

sber_debit = src.PlanFactory.create_debit_plan(src.TransferLimit(1e6, 1e4))
sber.add_plan(sber_debit.id)
sber_debit_model = src.Adaptor().create_plan(sber_debit, sber_model, "Sberbank debit plan")

sber_deposit = src.PlanFactory.create_deposit_plan(src.TransferLimit(1e6, 1e4), src.Period(5, 10), src.Commission(0.1, 0.2))
sber.add_plan(sber_deposit.id)
sber_deposit_model = src.Adaptor().create_plan(sber_deposit, sber_model, "Sberbank deposit plan")

sber_credit = src.PlanFactory.create_credit_plan(src.TransferLimit(1e6, 1e4), src.LowerLimit(-3e5, -3e3), src.Commission(-0.1, -0.2))
sber.add_plan(sber_credit.id)
sber_credit_model = src.Adaptor().create_plan(sber_credit, sber_model, "Sberbank credit plan")

tink_debit = src.PlanFactory.create_debit_plan(src.TransferLimit(1e6, 1e4))
tink.add_plan(tink_debit.id)
tink_debit_model = src.Adaptor().create_plan(sber_debit, sber_model, "Tinkoff deposit plan")

tink_deposit = src.PlanFactory.create_deposit_plan(src.TransferLimit(1e6, 1e4), src.Period(5, 10), src.Commission(0.1, 0.2))
tink.add_plan(tink_deposit.id)
tink_deposit_model = src.Adaptor().create_plan(sber_debit, sber_model, "Tinkoff deposit plan")

tink_credit = src.PlanFactory.create_credit_plan(src.TransferLimit(1e6, 1e4), src.LowerLimit(-3e5, -3e3), src.Commission(-0.1, -0.2))
tink.add_plan(tink_credit.id)
tink_credit_model = src.Adaptor().create_plan(sber_debit, sber_model, "Tinkoff deposit plan")

# Persons

denis = src.Person("20xygen", "1234", "Denis", "Barilov", "barilov.di@phystech.edu", "1234 123456")
denis_model = src.Adaptor().create_person(denis)

misha = src.Person("mikali", "lol", "Mikhail", "Kalinin", "kalinin.mi@phystech.edu", "0000 000000")
misha_model = src.Adaptor().create_person(misha)

artem = src.Person("artudo", "kek", "Artem", "Udovenko", "udovenko.ai@phystech.edu", "7777 777777")
artem_model = src.Adaptor().create_person(artem)

# Clients

denis_sber_id = sber.register(denis.name, denis.surname, denis.address, denis.passport)
denis_sber = src.DataOperator().get(denis_sber_id, "Client")
src.DataOperator().done_with(denis_sber_id, "Client")
denis_sber_model = src.Adaptor().create_client(denis_sber, sber_model, denis_model)

misha_sber_id = sber.register(misha.name, misha.surname)
misha_sber = src.DataOperator().get(misha_sber_id, "Client")
src.DataOperator().done_with(misha_sber_id, "Client")
misha_sber_model = src.Adaptor().create_client(misha_sber, sber_model, misha_model)

artem_sber_id = sber.register(artem.name, artem.surname)
artem_sber = src.DataOperator().get(artem_sber_id, "Client")
src.DataOperator().done_with(artem_sber_id, "Client")
artem_sber_model = src.Adaptor().create_client(artem_sber, sber_model, artem_model)

denis_tink_id = tink.register(denis.name, denis.surname, denis.address, denis.passport)
denis_tink = src.DataOperator().get(denis_tink_id, "Client")
src.DataOperator().done_with(denis_tink_id, "Client")
denis_tink_model = src.Adaptor().create_client(denis_tink, tink_model, denis_model)

misha_tink_id = tink.register(misha.name, misha.surname, misha.address, misha.passport)
misha_tink = src.DataOperator().get(misha_tink_id, "Client")
src.DataOperator().done_with(misha_tink_id, "Client")
misha_tink_model = src.Adaptor().create_client(misha_tink, tink_model, misha_model)

# Accounts

denis_sber_debit_id = sber.open_account(denis_sber.id, sber_debit.id)
denis_sber_debit = src.DataOperator().get(denis_sber_debit_id, "Account")
src.DataOperator().done_with(denis_sber_debit_id, "Account")
denis_sber_debit_model = src.Adaptor().create_account(denis_sber_debit, sber_model, denis_sber_model, sber_debit_model)

denis_sber_deposit_id = sber.open_account(denis_sber.id, sber_deposit.id)
denis_sber_deposit = src.DataOperator().get(denis_sber_deposit_id, "Account")
src.DataOperator().done_with(denis_sber_deposit_id, "Account")
denis_sber_deposit_model = src.Adaptor().create_account(denis_sber_deposit, sber_model, denis_sber_model, sber_deposit_model)

denis_sber_credit_id = sber.open_account(denis_sber.id, sber_credit.id)
denis_sber_credit = src.DataOperator().get(denis_sber_credit_id, "Account")
src.DataOperator().done_with(denis_sber_credit_id, "Account")
denis_sber_credit_model = src.Adaptor().create_account(denis_sber_credit, sber_model, denis_sber_model, sber_credit_model)

denis_tink_debit_id = tink.open_account(denis_tink.id, tink_debit.id)
denis_tink_debit = src.DataOperator().get(denis_tink_debit_id, "Account")
src.DataOperator().done_with(denis_tink_debit_id, "Account")
denis_tink_debit_model = src.Adaptor().create_account(denis_tink_debit, tink_model, denis_tink_model, tink_debit_model)

denis_tink_deposit_id = tink.open_account(denis_tink.id, tink_deposit.id)
denis_tink_deposit = src.DataOperator().get(denis_tink_deposit_id, "Account")
src.DataOperator().done_with(denis_tink_deposit_id, "Account")
denis_tink_deposit_model = src.Adaptor().create_account(denis_tink_deposit, tink_model, denis_tink_model, tink_deposit_model)

denis_tink_credit_id = tink.open_account(denis_tink.id, tink_credit.id)
denis_tink_credit = src.DataOperator().get(denis_tink_credit_id, "Account")
src.DataOperator().done_with(denis_tink_credit_id, "Account")
denis_tink_credit_model = src.Adaptor().create_account(denis_tink_credit, tink_model, denis_tink_model, tink_credit_model)


misha_sber_debit_id = sber.open_account(misha_sber.id, sber_debit.id)
misha_sber_debit = src.DataOperator().get(misha_sber_debit_id, "Account")
src.DataOperator().done_with(misha_sber_debit_id, "Account")
misha_sber_debit_model = src.Adaptor().create_account(misha_sber_debit, sber_model, misha_sber_model, sber_debit_model)

misha_sber_deposit_id = sber.open_account(misha_sber.id, sber_deposit.id)
misha_sber_deposit = src.DataOperator().get(misha_sber_deposit_id, "Account")
src.DataOperator().done_with(misha_sber_deposit_id, "Account")
misha_sber_deposit_model = src.Adaptor().create_account(misha_sber_deposit, sber_model, misha_sber_model, sber_deposit_model)

misha_tink_debit_id = tink.open_account(misha_tink.id, tink_debit.id)
misha_tink_debit = src.DataOperator().get(misha_tink_debit_id, "Account")
src.DataOperator().done_with(misha_tink_debit_id, "Account")
misha_tink_debit_model = src.Adaptor().create_account(misha_tink_debit, tink_model, misha_tink_model, tink_debit_model)


misha_tink_credit_id = tink.open_account(misha_tink.id, tink_credit.id)
misha_tink_credit = src.DataOperator().get(misha_tink_credit_id, "Account")
src.DataOperator().done_with(misha_tink_credit_id, "Account")
misha_tink_credit_model = src.Adaptor().create_account(misha_tink_credit, tink_model, misha_tink_model, tink_credit_model)


artem_sber_debit_id = sber.open_account(artem_sber.id, sber_debit.id)
artem_sber_debit = src.DataOperator().get(artem_sber_debit_id, "Account")
src.DataOperator().done_with(artem_sber_debit_id, "Account")
artem_sber_debit_model = src.Adaptor().create_account(artem_sber_debit, sber_model, artem_sber_model, sber_debit_model)

artem_sber_deposit_id = sber.open_account(artem_sber.id, sber_deposit.id)
artem_sber_deposit = src.DataOperator().get(artem_sber_deposit_id, "Account")
src.DataOperator().done_with(artem_sber_deposit_id, "Account")
artem_sber_deposit_model = src.Adaptor().create_account(artem_sber_deposit, sber_model, artem_sber_model, sber_deposit_model)

artem_sber_credit_id = sber.open_account(artem_sber.id, sber_credit.id)
artem_sber_credit = src.DataOperator().get(artem_sber_credit_id, "Account")
src.DataOperator().done_with(artem_sber_credit_id, "Account")
artem_sber_credit_model = src.Adaptor().create_account(artem_sber_credit, sber_model, artem_sber_model, sber_credit_model)
