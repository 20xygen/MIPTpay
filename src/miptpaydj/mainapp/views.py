from django.shortcuts import render
from .models import BankModel, AccountModel, PlanModel, PersonModel, ClientModel, TransactionModel

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


from django.shortcuts import render
from django.http import HttpResponse


def success(request):
    return HttpResponse("Operation Successful")


def deposit(request):
    if request.method == 'POST':
        bank = request.POST.get('bank')
        account_id = request.POST.get('account_id')
        amount = request.POST.get('amount')

        # logic

        return success(request)
    else:
        # Здесь нужно передать список банков и другие необходимые данные в шаблон
        return render(request, 'deposit.html', {})


def withdraw(request):
    if request.method == 'POST':
        bank = request.POST.get('bank')
        account_id = request.POST.get('account_id')
        amount = request.POST.get('amount')

        # logic

        return success(request)
    else:
        # Здесь нужно передать список банков и другие необходимые данные в шаблон
        return render(request, 'withdraw.html', {})


def transfer(request):
    if request.method == 'POST':
        from_bank = request.POST.get('from_bank')
        from_account_id = request.POST.get('from_account_id')
        to_account_id = request.POST.get('to_account_id')
        amount = request.POST.get('amount')

        # logic

        return success(request)
    else:
        # Здесь нужно передать список банков и другие необходимые данные в шаблон
        return render(request, 'transfer.html', {})


def interbank_transfer(request):
    if request.method == 'POST':
        from_bank = request.POST.get('from_bank')
        to_bank = request.POST.get('to_bank')
        from_account_id = request.POST.get('from_account_id')
        to_account_id = request.POST.get('to_account_id')
        amount = request.POST.get('amount')

        # logic

        return success(request)
    else:
        # Здесь нужно передать список банков и другие необходимые данные в шаблон
        return render(request, 'interbank_transfer.html', {})


def change_day(request):
    if request.method == 'POST':

        return success(request)
    else:
        return render(request, 'change_day.html', {})

