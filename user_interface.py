from user import *


class UserInterface:
    # Переписать на уже созданный класс
    __user: User

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
            self.__user.register(login, password, name, surname, address, passport)
        elif answer == 2:
            login = str(input("Введите ваш логин:"))
            password = str(input("Введите ваш пароль:"))
            self.__user.login(login, password)

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
            #TODO: Открытие депозита
            pass
        elif answer == 2:
            #TODO: Открытие кредита
            pass
        elif answer == 3:
            self.main_menu()
        else:
            print("Такого варианта нет попробуйте ещё раз")

    def profile(self):
        print("""Это страница вашего профиля
                 Ваши данные:""")
        print("Ваше имя:")
        print("Ваша фамилия:")
        print("Ваш адресс:")
        print("Ваш паспорт:")
        # TODO: Дописать для нового класса
        print("1.Вернуться в главное меню")
        answer = int(input("Введите 1:"))
        if answer == 1:
            self.main_menu()
        else:
            print("Такого варианта нет")
            self.profile()


    def main_menu(self):
        print("""Это главное меню приложения вы можете сделать следующее:
                    1.Зарегистрироваться в банке
                    2.Открыть счёт
                    3.Дополнить данные
                    4.Профиль""")
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
        else:
            print()


