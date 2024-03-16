from person import *
from dataoperator import *
from plan import *

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
        answer = int(input("Введите 1 или 2:"))
        if answer == 1:
            login = str(input("Придумайте логин:"))
            password = str(input("Придумайте пароль:"))
            name = str(input("Введите ваше имя:"))
            surname = str(input("Введите вашу фамилию:"))
            address = str(input("Введите ваш адрес:"))
            passport = int(input("Введите ваш номер паспорта:"))
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
        # TODO: У каждого банка могут быть по нескольку планов разных категорий (реализуй выбор среди таковых)
        print("""Это меню открытия счёта пожалуйста введите банк в котором вы хотите открыть счёт: """)
        bank_name = str(input())
        bank = DataOperator().get_bank_by_name(bank_name)
        print("Выберите счёт из предлагаемых данным банком:")
        planss: Dict[int, []] = {}
        counter = 1
        for ident in bank.plans:
            plan = DataOperator().get(ident, "Plan")
            planss[counter] = plan.get_properties()
            if isinstance(plan, DebitPlan):
                planss[counter].append("Дебетовый тариф")
            elif isinstance(plan, DepositPlan):
                planss[counter].append("Депозитный тариф")
            elif isinstance(plan, CreditPlan):
                planss[counter].append("Кредитный тариф")
            planss[counter].append(plan)
            counter += 1
        for i, plan in planss:
            # TODO: преназвать параметры
            properties = plan.get_properties()
            for p in properties:
                print(p.info())
            # print(i, ") Тип: ", plan[3], " Параметр 1: ", plan[0], " Параметр 2: ", plan[1], " Параметр 3: ", plan[2])
        ans = int(input("Введите номер:"))
        plan = planss[ans][4]
        client_id = self.__user.banks[bank]
        new_account = bank.open_account(client_id, plan)
        self.__user.accounts[bank_name] = new_account
        print("Новый счёт успешно открыт")
        self.main_menu()

    def profile(self):
        print("""Это страница вашего профиля
                     Ваши данные:""")
        print("Ваше имя: ", self.__user.name)
        print("Ваша фамилия: ", self.__user.surname)
        print("Ваш адрес: ", self.__user.address)
        print("Ваш паспорт: ", self.__user.passport)
        print("Открытые счета: ")
        for bank, account_id in self.__user.accounts:
            print(bank, ": параметры...")
        # TODO: Реализовать нормальный вывод счетов
        print("1. Вернуться в главное меню")
        answer = int(input("Введите 1:"))
        if answer == 1:
            self.main_menu()
        else:
            print("Такого варианта нет")
            self.profile()


    def operations(self):
        print("Это страница операций")
        print("Ваши счета:")
        # TODO: Вывод счетов
        account_num = int(input("Введите с каким счётом вы хотите совершить операцию:"))
        print("""Возможные дествия со счетами:
                     1. Полжить деньги
                     2. Снять деньги
                     3. Перевести со счёта на счёт
                     4. Закрыть счёт
                     5. Главное меню""")
        answer = int(input("Введите число от 1 до 5:"))
        if answer == 1:
            # sberbank - bank object, den_basic - account id
            # sberbank.put(den_basic, 100000)
            pass
        elif answer == 2:
            # sberbank - bank object, den_basic - account id
            # sberbank.get(den_basic, 100000)
            pass
        elif answer == 3:
            # sberbank - bank object, den_basic and misha_deposit - account id-s
            # sberbank.transfer(den_basic, misha_deposit, 10000)
            # TODO: there is also the way to make cross-bank transactions
            # denis, sberbank.id and den_basic - sender's info; tinkoff.id and artem_basic - responder's info; done - boolean indicator
            # done = crosspayment.get().transfer(sberbank.id, den_basic, tinkoff.id, artem_basic, denis, 5000)
            pass
        elif answer == 4:
            # not realized yet
            # TODO: account closing
            pass
        elif answer == 5:
            self.main_menu()
        else:
            print("Такого варианта нет")
            self.operations()


    def registration(self):
        print("Введите название банка в котором вы хотите зарегистрироваться:")
        bank_name = str(input())
        try:
            bank = DataOperator().get_bank_by_name(bank_name)
            new_id = bank.register(self.__user.name, self.__user.surname, self.__user.address,
                                   str(self.__user.passport))
            self.__user.banks[bank.name] = new_id
            print("Вы успешно зарегистрировались")
            self.main_menu()
        except:
            print("Такого банка не существует")
            self.main_menu()


    def update_data(self):
        if self.__user.banks:
            print("Введите название банка в котором вы хотите зменить данные:")
            bank_name = str(input())
            bank = DataOperator().get_bank_by_name(bank_name)
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
            try:
                bank.update(self.__user.banks[bank.name], address, passport)
                print("Данные успешно изменены")
                self.main_menu()
            except:
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
        answer = int(input("Введите число от 1 до 4:"))
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
            print()
