from src import (Bank, PlanFactory, TransferLimit, LowerLimit, Period, Commission, DataOperator, TimeKeeper,
                 Admin)
from src.banking import crosspayment

""" Testing module. """


sberbank = Bank("Sberbank")
sber_debit = sberbank.add_plan(PlanFactory.create_debit_plan(TransferLimit(1e6, 1e4)))
sber_credit = sberbank.add_plan(PlanFactory.create_credit_plan(TransferLimit(1e6, 1e4), LowerLimit(-3e5, -3e3), Commission(-0.1, -0.2)))
sber_deposit = sberbank.add_plan(PlanFactory.create_deposit_plan(TransferLimit(1e6, 1e4), Period(5, 10), Commission(0.1, 0.2)))
tinkoff = Bank("Tinkoff")
tink_debit = tinkoff.add_plan(PlanFactory.create_debit_plan(TransferLimit(1e6, 1e4)))
tink_credit = tinkoff.add_plan(PlanFactory.create_credit_plan(TransferLimit(1e6, 1e4), LowerLimit(-3e5, -3e3), Commission(-0.1, -0.2)))
tink_deposit = tinkoff.add_plan(PlanFactory.create_deposit_plan(TransferLimit(1e6, 1e4), Period(5, 10), Commission(0.1, 0.2)))

b = DataOperator().banks()
p = DataOperator().plans()
c = DataOperator().clients()
a = DataOperator().accounts()
t = DataOperator().transactions()
ct = TimeKeeper().current_time()


TimeKeeper().get()
TimeKeeper().increase()
print("Day 1 ------------------------\n")

denis = sberbank.register("Denis", "Barilov", "Moscow", "12 34 567890")
# print(denis)
den_basic = sberbank.open_account(denis, sber_debit)
sberbank.put(den_basic, 100000)
den_credit = sberbank.open_account(denis, sber_credit)
sberbank.get(den_credit, 50000)
den_deposit = sberbank.open_account(denis, sber_deposit)
sberbank.put(den_deposit, 150000)

print(DataOperator().account_info())


TimeKeeper().get()
TimeKeeper().increase()
print("Day 2 ------------------------\n")

misha = sberbank.register("Mikhail", "Kalinin")
misha_credit = sberbank.open_account(misha, sber_credit)
sberbank.get(misha_credit, 50000)
misha_deposit = sberbank.open_account(misha, sber_deposit)
sberbank.put(misha_deposit, 15000000000)

print(DataOperator().account_info())


TimeKeeper().get()
TimeKeeper().increase()
print("Day 3 ------------------------\n")

artem = tinkoff.register("Artem", "Udovenko")
artem_basic = tinkoff.open_account(artem, tink_debit)
tinkoff.put(artem_basic, 5000)

print(DataOperator().account_info())


TimeKeeper().get()
TimeKeeper().increase()
print("Day 4 ------------------------\n")

sberbank.update(misha, "Dolgoprudny", "9999999999")
sberbank.transfer(den_basic, misha_deposit, 10000)

print(DataOperator().account_info())


TimeKeeper().get()
TimeKeeper().increase()
print("Day 5 ------------------------\n")

done = crosspayment.get_cpf().transfer(sberbank.id, den_basic, tinkoff.id, artem_basic, denis, 5000)
print(done)

print(DataOperator().account_info())


more = input("More days?[Y/n]")
if more not in ["", "Y", "Yes"]:
    exit()

TimeKeeper().get()
TimeKeeper().increase()
print("Day 6 ------------------------\n")

print(DataOperator().account_info())


TimeKeeper().get()
TimeKeeper().increase()
print("Day 7 ------------------------\n")

print(DataOperator().account_info())


TimeKeeper().get()
TimeKeeper().increase()
print("Day 8 ------------------------\n")

print(DataOperator().account_info())

print(Admin().account_info(den_credit))
print(Admin().plan_info(sber_debit))
print(Admin().client_info(denis))
print(Admin().bank_info(sberbank.id))

