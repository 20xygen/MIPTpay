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
                    2. Войти""")
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
            address = str(input("Введите ваш адрес:"))
            passport = str(input("Введите ваш номер паспорта (Формат: 00 00 000000):"))
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
        for bank_name, account_id in self.__user.accounts:
            plan = DataOperator().get(account_id, "Plan")
            properties = plan.get_properties()
            print("Ваш счёт банка: ", bank_name, "Номер счёта: ", account_id)
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
        elif ans == 2:
            # TODO: функция будет работать только если человек клиент только одно банка...
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
        elif ans == 3:
            self.operations()
        else:
            print("Такого варианта нет:")
            self.transaction(account_id, bank)

    def operations(self):
        print("Это страница операций")
        print("Ваши счета:")
        planss: Dict[int, Plan] = {}
        counter = 1
        for ident in self.__user.accounts:
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
            print(counter, ") ", plan_type, " Номер счёта: ", ident)
            for p in properties:
                print(p.info())
            counter += 1
        try:
            account_num = int(input("Введите номер счёта с которым вы хотите совершить операцию:"))
        except:
            print("Пожалуйста введите число!")
            self.operations()
        account_id = planss[account_num].id
        global_bank_name = ""
        for bank_name, ident in self.__user.banks:
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
        elif answer == 2:
            try:
                s = int(input("Введите сумму для снятия:"))
            except:
                print("Пожалуйста введите число!")
                self.operations()
            bank.put(account_id, s)
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
                        6. Выход""")
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
            exit(0)
        else:
            print("Введено неверное число")
            self.main_menu()
