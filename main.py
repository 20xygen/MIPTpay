import timekeeper
from plan import Plan, DepositPlan, CreditPlan
import dataoperator
from bank import Bank


sberbank = Bank("Sberbank")
sber_credit = sberbank.add_plan(CreditPlan(-300000, -50000, 0.1, 0.2))
sber_deposit = sberbank.add_plan(DepositPlan(3, 0.2, 0.3))
tinkoff = Bank("Tinkoff")
tink_credit = tinkoff.add_plan(CreditPlan(-500000, -70000, 0.1, 0.2))
tink_deposit = tinkoff.add_plan(DepositPlan(5, 0.1, 0.2))

b = dataoperator.banks
p = dataoperator.plans
c = dataoperator.clients
a = dataoperator.accounts
t = dataoperator.transactions
ct = timekeeper.current_time


timekeeper.get()
timekeeper.increase()
print("Day 1 ------------------------\n")

denis = sberbank.register("Denis", "Barilov", "Moscow", 1122333444)
den_basic = sberbank.open_account(denis)
sberbank.put(den_basic, 100000)
den_credit = sberbank.open_account(denis, sber_credit)
sberbank.get(den_credit, 50000)
den_deposit = sberbank.open_account(denis, sber_deposit)
sberbank.put(den_deposit, 150000)

print(dataoperator.account_info())


timekeeper.get()
timekeeper.increase()
print("Day 2 ------------------------\n")

misha = sberbank.register("Mikhail", "Kalinin")
misha_credit = sberbank.open_account(misha, sber_credit)
sberbank.get(misha_credit, 50000)
misha_deposit = sberbank.open_account(misha, sber_deposit)
sberbank.put(misha_deposit, 150000)

print(dataoperator.account_info())


timekeeper.get()
timekeeper.increase()
print("Day 3 ------------------------\n")

artem = tinkoff.register("Artem", "Udovenko")
artem_basic = tinkoff.open_account(artem)
tinkoff.put(artem_basic, 100000)

print(dataoperator.account_info())


timekeeper.get()
timekeeper.increase()
print("Day 4 ------------------------\n")

sberbank.update(misha, "Dolgoprudny", 9999999999)

sberbank.transfer(den_basic, misha_deposit, 10000)

print(dataoperator.account_info())


timekeeper.get()
timekeeper.increase()
print("Day 5 ------------------------\n")

print(dataoperator.account_info())


timekeeper.get()
timekeeper.increase()
print("Day 6 ------------------------\n")

print(dataoperator.account_info())


timekeeper.get()
timekeeper.increase()
print("Day 7 ------------------------\n")

print(dataoperator.account_info())


timekeeper.get()
timekeeper.increase()
print("Day 8 ------------------------\n")

print(dataoperator.account_info())