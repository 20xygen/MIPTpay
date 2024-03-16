from person import *


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
        print("""Это меню открытия счёта пожалуйста выберете счёт который вы хотите открыть:
                  1. Дебитовый счет
                  2. Депозитный счет
                  3. Кредитный счет
                  4. Главное меню""")
        answer = int(input("Введите 1, 2, 3:"))
        if answer == 1:
            # den_basic - new account's id; sberbank - bank object; denis - client id; sber_debit - plan id
            # den_basic = sberbank.open_account(denis, sber_debit)
            pass
        elif answer == 2:
            # den_deposit - new account's id; sberbank - bank object; denis - client id; sber_deposit - plan id
            # den_deposit = sberbank.open_account(denis, sber_deposit)
            pass
        elif answer == 3:
            # den_credit - new account's id; sberbank - bank object; denis - client id; sber-credit - plan id
            # den_credit = sberbank.open_account(denis, sber_credit)
            pass
        elif answer == 4:
            self.main_menu()
        else:
            print("Такого варианта нет попробуйте ещё раз")

    def profile(self):
        print("""Это страница вашего профиля
                 Ваши данные:""")
        print("Ваше имя: ", self.__user.name)
        print("Ваша фамилия: ", self.__user.surname)
        print("Ваш адресс: ", self.__user.address)
        print("Ваш паспорт: ", self.__user.passport)
        print("Открытые счета: ")
        # TODO: Реализовать нормальный вывод счетов
        for i in range(self.__user.plans.size()):
            print(i, ") ", self.__user.plans[i])
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
            # denis - new client's id; sberbank - bank object
            # denis = sberbank.register("Denis", "Barilov", "Moscow", "12 34 567890")
            pass
        elif answer == 2:
            self.open_plan()
        elif answer == 3:
            # misha - new client's id; sberbank - bank object
            # sberbank.update(misha, "Dolgoprudny", "9999999999")
            pass
        elif answer == 4:
            self.profile()
        elif answer == 5:
            self.operations()
        elif answer == 6:
            exit(0)
        else:
            print()
