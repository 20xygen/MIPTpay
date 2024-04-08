from django.shortcuts import render
from src.miptpaydj.mainapp.models import BankModel, AccountModel, PlanModel, PersonModel, ClientModel, TransactionModel
import src

def banks(request):
    banks = BankModel.objects.all()
    return render(request, 'banks.html', {'banks': banks})

def accounts(request):
    accounts = AccountModel.objects.all()
    return render(request, 'accounts.html', {'accounts': accounts})

def plans(request):
    plans = PlanModel.objects.all()
    return render(request, 'plans.html', {'plans': plans})

def persons(request):
    persons = PersonModel.objects.all()
    return render(request, 'persons.html', {'persons': persons})

def clients(request):
    clients = ClientModel.objects.all()
    return render(request, 'clients.html', {'clients': clients})

def transactions(request):
    transactions = TransactionModel.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions})

def hello_world(request):
    return render(request, 'index.html', {'greeting': 'Hello, world!'})

