import src
from django.contrib.auth import authenticate, login

src.User.objects.all().delete()
src.DiaryModel.objects.all().delete()
src.BankModel.objects.all().delete()
src.PersonModel.objects.all().delete()
src.ClientModel.objects.all().delete()
src.PlanCategoryModel.objects.all().delete()
src.PlanModel.objects.all().delete()
src.AccountModel.objects.all().delete()
src.TransactionModel.objects.all().delete()

# Date

src.Adaptor().set_date()

# Plan categories

debit = src.PlanCategoryModel(name="Debit", commission=False, period=False, lower_limit=False, upper_limit=False, transfer_limit=True)
debit.save()
deposit = src.PlanCategoryModel(name="Deposit", commission=True, period=True, lower_limit=False, upper_limit=False, transfer_limit=True)
deposit.save()
credit = src.PlanCategoryModel(name="Credit", commission=True, period=False, lower_limit=True, upper_limit=False, transfer_limit=True)
credit.save()

# Banks

sber = src.Bank(None, "Sberbank")
# sber_model = src.Adaptor().create_bank(sber)

tink = src.Bank(None,"Tinkoff")
# tink_model = src.Adaptor().create_bank(tink)

# Plans

sber_debit = src.PlanFactory.create_debit_plan(src.TransferLimit(1e6, 1e4), sber.id)
sber.add_plan(sber_debit.id)
# sber_debit_model = src.Adaptor().create_plan(sber_debit, sber_model)

sber_deposit = src.PlanFactory.create_deposit_plan(src.TransferLimit(1e6, 1e4), src.Period(5, 10), src.Commission(0.1, 0.2), sber.id)
sber.add_plan(sber_deposit.id)
# sber_deposit_model = src.Adaptor().create_plan(sber_deposit, sber_model)

sber_credit = src.PlanFactory.create_credit_plan(src.TransferLimit(1e6, 1e4), src.LowerLimit(-3e5, -3e3), src.Commission(-0.1, -0.2), sber.id)
sber.add_plan(sber_credit.id)
# sber_credit_model = src.Adaptor().create_plan(sber_credit, sber_model)

tink_debit = src.PlanFactory.create_debit_plan(src.TransferLimit(1e6, 1e4), tink.id)
tink.add_plan(tink_debit.id)
# tink_debit_model = src.Adaptor().create_plan(sber_debit, sber_model)

tink_deposit = src.PlanFactory.create_deposit_plan(src.TransferLimit(1e6, 1e4), src.Period(5, 10), src.Commission(0.1, 0.2), tink.id)
tink.add_plan(tink_deposit.id)
# tink_deposit_model = src.Adaptor().create_plan(sber_debit, sber_model)

tink_credit = src.PlanFactory.create_credit_plan(src.TransferLimit(1e6, 1e4), src.LowerLimit(-3e5, -3e3), src.Commission(-0.1, -0.2), tink.id)
tink.add_plan(tink_credit.id)
# tink_credit_model = src.Adaptor().create_plan(sber_debit, sber_model)

# Persons and Users

xygen = src.User.objects.create_user(username='xygen', password='strong_password')
mikali = src.User.objects.create_user(username='mikali', password='ordinary_password')
artudi = src.User.objects.create_user(username='artudi', password='weak_password')

xygen.save()
mikali.save()
artudi.save()

xygen.refresh_from_db()
mikali.refresh_from_db()
artudi.refresh_from_db()

denis = src.Person(ident=xygen.personmodel.id, name="Denis", surname="Barilov", address="barilov.di@phystech.edu", passport="1234 123456")
# denis_model = src.Adaptor().create_person(denis, xygen)
src.Adaptor().fill_person(xygen.personmodel, denis)
denis_model = xygen.personmodel

misha = src.Person(ident=mikali.personmodel.id, name="Mikhail", surname="Kalinin", address="kalinin.mi@phystech.edu", passport="1000 000000")
# misha_model = src.Adaptor().create_person(misha, mikali)
src.Adaptor().fill_person(mikali.personmodel, misha)
misha_model = mikali.personmodel

artem = src.Person(ident=artudi.personmodel.id, name="Artem", surname="Udovenko", address="udovenko.ai@phystech.edu", passport="7777 777777")
# artem_model = src.Adaptor().create_person(artem, artudi)
src.Adaptor().fill_person(artudi.personmodel, artem)
artem_model = artudi.personmodel

xygen.save()
mikali.save()
artudi.save()

xygen = authenticate(username=xygen.username, password=xygen.password)
mikali = authenticate(username=mikali.username, password=mikali.password)
artudi = authenticate(username=artudi.username, password=artudi.password)


# Clients

denis_sber_id = sber.register(denis.name, denis.surname, denis.address, denis.passport, denis.id)
# denis_sber = src.DataOperator().get(denis_sber_id, "Client")
# src.DataOperator().done_with(denis_sber_id, "Client")
# denis_sber_model = src.Adaptor().create_client(denis_sber, sber_model, denis_model)

misha_sber_id = sber.register(misha.name, misha.surname, "NO_VALUE", "NO_VALUE", misha.id)
# misha_sber = src.DataOperator().get(misha_sber_id, "Client")
# src.DataOperator().done_with(misha_sber_id, "Client")
# misha_sber_model = src.Adaptor().create_client(misha_sber, sber_model, misha_model)

artem_sber_id = sber.register(artem.name, artem.surname, "NO_VALUE", "NO_VALUE", artem.id)
# artem_sber = src.DataOperator().get(artem_sber_id, "Client")
# src.DataOperator().done_with(artem_sber_id, "Client")
# artem_sber_model = src.Adaptor().create_client(artem_sber, sber_model, artem_model)

denis_tink_id = tink.register(denis.name, denis.surname, denis.address, denis.passport, denis.id)
# denis_tink = src.DataOperator().get(denis_tink_id, "Client")
# src.DataOperator().done_with(denis_tink_id, "Client")
# denis_tink_model = src.Adaptor().create_client(denis_tink, tink_model, denis_model)

misha_tink_id = tink.register(misha.name, misha.surname, misha.address, misha.passport, misha.id)
# misha_tink = src.DataOperator().get(misha_tink_id, "Client")
# src.DataOperator().done_with(misha_tink_id, "Client")
# misha_tink_model = src.Adaptor().create_client(misha_tink, tink_model, misha_model)

# Accounts

denis_sber_debit_id = sber.open_account(denis_sber_id, sber_debit.id)
# denis_sber_debit = src.DataOperator().get(denis_sber_debit_id, "Account")
# src.DataOperator().done_with(denis_sber_debit_id, "Account")
# denis_sber_debit_model = src.Adaptor().create_account(denis_sber_debit, sber_model, denis_sber_model, sber_debit_model)

denis_sber_deposit_id = sber.open_account(denis_sber_id, sber_deposit.id)
# denis_sber_deposit = src.DataOperator().get(denis_sber_deposit_id, "Account")
# src.DataOperator().done_with(denis_sber_deposit_id, "Account")
# denis_sber_deposit_model = src.Adaptor().create_account(denis_sber_deposit, sber_model, denis_sber_model, sber_deposit_model)

denis_sber_credit_id = sber.open_account(denis_sber_id, sber_credit.id)
# denis_sber_credit = src.DataOperator().get(denis_sber_credit_id, "Account")
# src.DataOperator().done_with(denis_sber_credit_id, "Account")
# denis_sber_credit_model = src.Adaptor().create_account(denis_sber_credit, sber_model, denis_sber_model, sber_credit_model)

denis_tink_debit_id = tink.open_account(denis_tink_id, tink_debit.id)
# denis_tink_debit = src.DataOperator().get(denis_tink_debit_id, "Account")
# src.DataOperator().done_with(denis_tink_debit_id, "Account")
# denis_tink_debit_model = src.Adaptor().create_account(denis_tink_debit, tink_model, denis_tink_model, tink_debit_model)

denis_tink_deposit_id = tink.open_account(denis_tink_id, tink_deposit.id)
# denis_tink_deposit = src.DataOperator().get(denis_tink_deposit_id, "Account")
# src.DataOperator().done_with(denis_tink_deposit_id, "Account")
# denis_tink_deposit_model = src.Adaptor().create_account(denis_tink_deposit, tink_model, denis_tink_model, tink_deposit_model)

denis_tink_credit_id = tink.open_account(denis_tink_id, tink_credit.id)
# denis_tink_credit = src.DataOperator().get(denis_tink_credit_id, "Account")
# src.DataOperator().done_with(denis_tink_credit_id, "Account")
# denis_tink_credit_model = src.Adaptor().create_account(denis_tink_credit, tink_model, denis_tink_model, tink_credit_model)


misha_sber_debit_id = sber.open_account(misha_sber_id, sber_debit.id)
# misha_sber_debit = src.DataOperator().get(misha_sber_debit_id, "Account")
# src.DataOperator().done_with(misha_sber_debit_id, "Account")
# misha_sber_debit_model = src.Adaptor().create_account(misha_sber_debit, sber_model, misha_sber_model, sber_debit_model)

misha_sber_deposit_id = sber.open_account(misha_sber_id, sber_deposit.id)
# misha_sber_deposit = src.DataOperator().get(misha_sber_deposit_id, "Account")
# src.DataOperator().done_with(misha_sber_deposit_id, "Account")
# misha_sber_deposit_model = src.Adaptor().create_account(misha_sber_deposit, sber_model, misha_sber_model, sber_deposit_model)

misha_tink_debit_id = tink.open_account(misha_tink_id, tink_debit.id)
# misha_tink_debit = src.DataOperator().get(misha_tink_debit_id, "Account")
# src.DataOperator().done_with(misha_tink_debit_id, "Account")
# misha_tink_debit_model = src.Adaptor().create_account(misha_tink_debit, tink_model, misha_tink_model, tink_debit_model)


misha_tink_credit_id = tink.open_account(misha_tink_id, tink_credit.id)
# misha_tink_credit = src.DataOperator().get(misha_tink_credit_id, "Account")
# src.DataOperator().done_with(misha_tink_credit_id, "Account")
# misha_tink_credit_model = src.Adaptor().create_account(misha_tink_credit, tink_model, misha_tink_model, tink_credit_model)


artem_sber_debit_id = sber.open_account(artem_sber_id, sber_debit.id)
# artem_sber_debit = src.DataOperator().get(artem_sber_debit_id, "Account")
# src.DataOperator().done_with(artem_sber_debit_id, "Account")
# artem_sber_debit_model = src.Adaptor().create_account(artem_sber_debit, sber_model, artem_sber_model, sber_debit_model)

artem_sber_deposit_id = sber.open_account(artem_sber_id, sber_deposit.id)
# artem_sber_deposit = src.DataOperator().get(artem_sber_deposit_id, "Account")
# src.DataOperator().done_with(artem_sber_deposit_id, "Account")
# artem_sber_deposit_model = src.Adaptor().create_account(artem_sber_deposit, sber_model, artem_sber_model, sber_deposit_model)

artem_sber_credit_id = sber.open_account(artem_sber_id, sber_credit.id)
# artem_sber_credit = src.DataOperator().get(artem_sber_credit_id, "Account")
# src.DataOperator().done_with(artem_sber_credit_id, "Account")
# artem_sber_credit_model = src.Adaptor().create_account(artem_sber_credit, sber_model, artem_sber_model, sber_credit_model)
