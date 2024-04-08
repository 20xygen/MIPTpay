import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.miptpaydj.miptpaydj.settings')
# django.setup()

from src.tools.accesstools import available_from

from src.plan.planproperty import PlanProperty, Commission, Period, LowerLimit, UpperLimit, TransferLimit
from src.plan.plan import Plan, DebitPlan, DepositPlan, CreditPlan
from src.plan.planfactory import PlanFactory

from src.banking.client import Client
from src.banking.clientbuilder import ClientBuilder

from src.account.account import Account, DebitAccount, DepositAccount, CreditAccount
from src.account.accountfactory import AccountFactory

from src.transaction.transaction import Transaction

from src.banking.bank import Bank
from src.banking.crosspaymentsystem import CrossPaymentSystem, system
from src.banking.crosspayment import get_cpf

from src.users.person import Person
from src.admin.admin import Admin

from src.operators.timekeeper import TimeKeeper
from src.operators.dataoperator import DataOperator

from src.interface.user_interface import UserInterface

from src.miptpaydj import mainapp
from src.miptpaydj import miptpaydj

from src.miptpaydj.mainapp.models import BankModel, PersonModel, ClientModel, PlanCategoryModel, PlanModel, AccountModel, TransactionModel, DiaryModel

# from plan.plancategory import PlanCategory

from src.operators.adapters import Adapter

from src.miptpaydj.mainapp import apps

from src.miptpaydj.mainapp import views

__all__ = ['available_from',
           'PlanProperty', 'Commission', 'Period', 'LowerLimit', 'UpperLimit', 'TransferLimit',
           'Plan', 'DebitPlan', 'DepositPlan', 'CreditPlan',
           'PlanFactory',
           'Client', 'ClientBuilder',
           'Account', 'DepositAccount', 'DebitAccount', 'CreditAccount',
           'AccountFactory',
           'Transaction',
           'Bank',
           'CrossPaymentSystem', 'system',
           'get_cpf',
           'TimeKeeper',
           'DataOperator',
           'Person',
           'Admin',
           'UserInterface',
           'mainapp', 'miptpaydj',
           'BankModel', 'PersonModel', 'ClientModel', 'PlanCategoryModel', 'PlanModel', 'AccountModel', 'TransactionModel', 'DiaryModel',
           'Adapter',
           'apps',
           'views',
           ]
