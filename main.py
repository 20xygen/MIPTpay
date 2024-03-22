from timekeeper import TimeKeeper
from planfactory import *
from dataoperator import DataOperator
from bank import Bank
from user_interface import *

""" Application execution. """

user_inter = UserInterface()
user_inter.bank_create()
user_inter.login_and_register()
