from person import *


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
        print("""Это меню открытия счёта пожалуйста выберете счёт который вы хотите открыть:
                  1. Депозит
                  2. Кредит
                  3. Главное меню""")
        answer = int(input("Введите 1, 2, 3:"))
        if answer == 1:
            # TODO: Открытие депозита (добавить этот счёт в массив)
            pass
        elif answer == 2:
            # TODO: Открытие кредита (добавть счёт в массив)
            pass
        elif answer == 3:
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
            # TODO: положить деньги
            pass
        elif answer == 2:
            # TODO: снять деньги
            pass
        elif answer == 3:
            # TODO: Перевод между счетами
            pass
        elif answer == 4:
            # TODO: Закрытие счёта
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
            # TODO: Регистрация в банке (Данные подгружаются из User вроде ничего дополнительного спрашивать не надо)
            pass
        elif answer == 2:
            self.open_plan()
        elif answer == 3:
            # TODO: Дополнить данные
            pass
        elif answer == 4:
            self.profile()
        elif answer == 5:
            self.operations()
        elif answer == 6:
            exit(0)
        else:
            print()
