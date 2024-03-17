import crosspayment
from person import *
from dataoperator import *
from plan import *
from planfactory import *

"""

print(DataOperator().account_info())  # print info about all accounts
TimeKeeper().get()  # to get current date
TimeKeeper().increase()  # go to next day (and update all accounts)

check out the main.py for complete understanding

"""


class UserInterface:
    __user: Person

    def login_and_register(self):
        print("""Вас приветствует MiptPay! Ваши действия:
                    1. Зарегестрироваться
                    2. Войти (в тестовом режиме эта функция недоступна)""")
        try:
            answer = int(input("Введите 1 или 2:"))
        except:
            print("Пожалуйста введите число!")
            self.login_and_register()
        if answer == 1:
            login = str(input("Придумайте логин:"))
            password = str(input("Придумайте пароль:"))
            name = str(input("Введите ваше имя:"))
            surname = str(input("Введите вашу фамилию:"))
            address = str(input("Введите ваш адрес (enter для пропуска):"))
            if len(address) < 1:
                print("Пропущен ввод адреса. Данные можно будет дополнить позднее.")
                address = None
            passport = str(input("Введите ваш номер паспорта (формат: 00 00 000000) (enter для пропуска):"))
            if len(passport) < 1:
                print("Пропущен ввод паспорта. Данные можно будет дополнить позднее.")
                passport = None
            self.__user = Person(login, password, name, surname, address, passport)
            self.main_menu()
        elif answer == 2:
            login = str(input("Введите ваш логин:"))
            password = str(input("Введите ваш пароль:"))
            self.__user.login(login, password)
            self.main_menu()
        else:
            print("Такого варианта нет, попробуйте ещё раз")
            self.login_and_register()

    def open_plan(self):
        print("""Это меню открытия счёта пожалуйста введите банк в котором вы хотите открыть счёт: """)
        bank_name = str(input())
        try:
            bank = DataOperator().get_bank_by_name(bank_name)
        except:
            print("Введённые банк не поддерживается нашей системой")
            self.open_plan()
        print("Выберите счёт из предлагаемых данным банком:")
        planss: Dict[int, Plan] = {}
        counter = 1
        for ident in bank.plans:
            plan = DataOperator().get(ident, "Plan")
            plan_type = ""
            if isinstance(plan, DebitPlan):
                plan_type = "Дебетовый тариф"
            elif isinstance(plan, DepositPlan):
                plan_type = "Депозитный тариф"
            elif isinstance(plan, CreditPlan):
                plan_type = "Кредитный тариф"
            planss[counter] = plan
            properties = plan.get_properties()
            print(counter, ") ", plan_type, ":")
            for p in properties:
                print(p.info())
            counter += 1
        try:
            ans = int(input("Введите номер:"))
        except:
            print("Пожалуйста введите число!")
            self.open_plan()
        if ans < counter:
            plan = planss[ans]
        else:
            print("Неверный номер:")
            self.main_menu()
        client_id = self.__user.banks[bank_name]
        new_account = bank.open_account(client_id, plan.id)
        if new_account is None:
            print("Такой счёт уже зарегистрирован")
            self.main_menu()
        self.__user.accounts[bank_name] = new_account
        self.__user.plans[new_account] = plan.id
        print("Новый счёт успешно открыт. Номер васшего счёта: ", new_account)
        self.main_menu()

    def profile(self):
        print("""Это страница вашего профиля
                     Ваши данные:""")
        print("Ваше имя: ", self.__user.name)
        print("Ваша фамилия: ", self.__user.surname)
        print("Ваш адрес: ", self.__user.address)
        print("Ваш паспорт: ", self.__user.passport)
        print("Открытые счета: ")
        for account_id, plan_id in self.__user.plans.items():
            plan = DataOperator().get(plan_id, "Plan")
            properties = plan.get_properties()
            print("Номер счёта: ", account_id)
            for p in properties:
                print(p.info())
        print("1. Вернуться в главное меню")
        try:
            answer = int(input("Введите 1:"))
        except:
            print("Пожалуйста введите число!")
            self.profile()
        if answer == 1:
            self.main_menu()
        else:
            print("Такого варианта нет")
            self.profile()

    def transaction(self, account_id: int, bank: Bank):
        print("Это страница перевода между счетами:"
              "1. В одном банке"
              "2. Между банками"
              "3. Назад")
        try:
            ans = int(input("Введите от 1 до 3:"))
        except:
            print("Пожалуйста введите число!")
            self.transaction(account_id, bank)
        if ans == 1:
            try:
                second_account_id = int(input("Введите номер счёта получателя:"))
            except:
                print("Пожалуйста введите число!")
                self.transaction(account_id, bank)
            try:
                s = int(input("Введите сумму перевода:"))
            except:
                print("Пожалуйста введите число!")
                self.transaction(account_id, bank)
            bank.transfer(account_id, second_account_id, s)
            print("Ваши деньги успешно переведены")
        elif ans == 2:
            second_bank_name = str(input("Введите банк получателя:"))
            try:
                second_bank = DataOperator().get_bank_by_name(second_bank_name)
            except:
                print("Такой банк не зарегистрирован")
                self.transaction(account_id, bank)
            try:
                second_account_id = int(input("Введите номер счёта получателя:"))
            except:
                print("Пожалуйста введите число!")
                self.transaction(account_id, bank)
            try:
                s = int(input("Введите сумму перевода:"))
            except:
                print("Пожалуйста введите число!")
                self.transaction(account_id, bank)
            acc = self.__user.banks[bank.name]
            crosspayment.get().transfer(bank.id, account_id, second_bank.id, second_account_id, acc, s)
            print("Ваши деньги успешно переведены")
        elif ans == 3:
            self.operations()
        else:
            print("Такого варианта нет:")
            self.transaction(account_id, bank)

    def operations(self):
        print("Это страница операций")
        print("Ваши счета:")
        for account_id, plan_id in self.__user.plans.items():
            plan = DataOperator().get(plan_id, "Plan")
            plan_type = ""
            if isinstance(plan, DebitPlan):
                plan_type = "Дебетовый тариф"
            elif isinstance(plan, DepositPlan):
                plan_type = "Депозитный тариф"
            elif isinstance(plan, CreditPlan):
                plan_type = "Кредитный тариф"
            properties = plan.get_properties()
            print("Номер счёта: ", account_id, "Тип: ", plan_type)
            for p in properties:
                print(p.info())
        try:
            account_id = int(input("Введите номер счёта с которым вы хотите совершить операцию:"))
        except:
            print("Пожалуйста введите число!")
            self.operations()
        global_bank_name = ""
        for bank_name, ident in self.__user.banks.items():
            if ident == account_id:
                global_bank_name = bank_name
        bank = DataOperator().get_bank_by_name(global_bank_name)
        print("""Возможные дествия со счетами:
                     1. Полжить деньги
                     2. Снять деньги
                     3. Перевести со счёта на счёт
                     4. Закрыть счёт
                     5. Главное меню""")
        try:
            answer = int(input("Введите число от 1 до 5:"))
        except:
            print("Пожалуйста введите число!")
            self.operations()
        if answer == 1:
            try:
                s = int(input("Введите сумму для зачисления:"))
            except:
                print("Пожалуйста введите число!")
                self.operations()
            bank.put(account_id, s)
            print("Ваши деньги успешно зачислены")
        elif answer == 2:
            try:
                s = int(input("Введите сумму для снятия:"))
            except:
                print("Пожалуйста введите число!")
                self.operations()
            bank.put(account_id, s)
            print("Ваши деньги успешно сняты")
        elif answer == 3:
            self.transaction(account_id, bank)
        elif answer == 4:
            print("Данная операция ещё не реализована")
            self.operations()
        elif answer == 5:
            self.main_menu()
        else:
            print("Такого варианта нет")
            self.operations()
        self.main_menu()

    def registration(self):
        print("Введите название банка в котором вы хотите зарегистрироваться:")
        bank_name = str(input())
        try:
            bank = DataOperator().get_bank_by_name(bank_name)
            new_id = bank.register(self.__user.name, self.__user.surname, self.__user.address,
                                   str(self.__user.passport))
            if new_id is None:
                print("Данные указаны в неверном формате")
            self.__user.banks[bank.name] = new_id
            print("Вы успешно зарегистрировались")
            self.main_menu()
        except:
            print("Такого банка не существует")
            self.main_menu()

    def update_data(self):
        if self.__user.banks:
            print("Введите название банка в котором вы хотите заменить данные:")
            bank_name = str(input())
            try:
                bank = DataOperator().get_bank_by_name(bank_name)
            except:
                print("Такого банка не существует")
                self.update_data()
            address = self.__user.address
            passport = str(self.__user.passport)
            print("Хотите поменять адрес: (Y/N)")
            ans = str(input())
            if ans == "Y":
                print("Введите адресс:")
                address = str(input())
            print("Хотите поменять паспорт: (Y/N)")
            ans = str(input())
            if ans == "Y":
                print("Введите паспорт:")
                passport = str(input())
            if bank.update(self.__user.banks[bank.name], address, passport):
                print("Данные успешно изменены")
            else:
                print("Вы не зарегистрированы в этом банке")
            self.main_menu()
        else:
            print("Вы не зарегистрированы ни в одном банке")
            self.main_menu()

    def main_menu(self):
        print("""Это главное меню приложения вы можете сделать следующее:
                        1. Зарегистрироваться в банке
                        2. Открыть счёт
                        3. Дополнить данные
                        4. Профиль
                        5. Операции со счётом
                        6. Перейти к следующему дню
                        7. Выход""")
        try:
            answer = int(input("Введите число от 1 до 4:"))
        except:
            print("Пожалуйста введите число!")
            self.main_menu()
        if answer == 1:
            self.registration()
        elif answer == 2:
            self.open_plan()
        elif answer == 3:
            self.update_data()
        elif answer == 4:
            self.profile()
        elif answer == 5:
            self.operations()
        elif answer == 6:
            __import__("timekeeper"). TimeKeeper().increase()
            print(DataOperator().account_info())
        elif answer == 7:
            exit(0)
        else:
            print("Введено неверное число")
            self.main_menu()

    def bank_create(self):
        sberbank = Bank("Sberbank")
        sber_debit = sberbank.add_plan(PlanFactory.create_debit_plan(TransferLimit(1e6, 1e4)))
        sber_credit = sberbank.add_plan(
            PlanFactory.create_credit_plan(TransferLimit(1e6, 1e4), LowerLimit(-3e5, -3e3), Commission(-0.1, -0.2)))
        sber_deposit = sberbank.add_plan(
            PlanFactory.create_deposit_plan(TransferLimit(1e6, 1e4), Period(5, 10), Commission(0.1, 0.2)))

        tinkoff = Bank("Tinkoff")
        tink_debit = tinkoff.add_plan(PlanFactory.create_debit_plan(TransferLimit(1e6, 1e4)))
        tink_credit = tinkoff.add_plan(
            PlanFactory.create_credit_plan(TransferLimit(1e6, 1e4), LowerLimit(-3e5, -3e3), Commission(-0.1, -0.2)))
        tink_deposit = tinkoff.add_plan(
            PlanFactory.create_deposit_plan(TransferLimit(1e6, 1e4), Period(5, 10), Commission(0.1, 0.2)))