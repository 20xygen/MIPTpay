from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from src.miptpaydj.mainapp.forms import RegisterForm, PutForm, TransferForm
from src.miptpaydj.mainapp.models import BankModel, AccountModel, PlanModel, PersonModel, ClientModel, TransactionModel

import src


def banks(request):
    src.SingleTK.timekeeper().update()
    banks = BankModel.objects.all()
    return render(request, 'banks.html', {'banks': banks})


def accounts(request):
    src.SingleTK.timekeeper().update()

    bank = src.SingleDO.DO().get(11, "Bank")
    bank.put(29, 100)
    src.SingleDO.DO().done_with(11, "Bank")

    bank = src.SingleDO.DO().get(12, "Bank")
    bank.get(36, 1000)
    src.SingleDO.DO().done_with(12, "Bank")

    accounts = AccountModel.objects.all()
    return render(request, 'accounts.html', {'accounts': accounts})


def plans(request):
    src.SingleTK.timekeeper().update()
    plans = PlanModel.objects.all()
    return render(request, 'plans.html', {'plans': plans})


def persons(request):
    src.SingleTK.timekeeper().update()
    persons = PersonModel.objects.all()
    return render(request, 'persons.html', {'persons': persons})


def clients(request):
    src.SingleTK.timekeeper().update()
    # bank = src.SingleDO.DO().get(3, "Bank")
    # bank.update(2, "kalinin.mi@phystech.edu", "1000 000000")
    # src.SingleDO.DO().done_with(3, "Bank")

    clients = ClientModel.objects.all()
    return render(request, 'clients.html', {'clients': clients})


def transactions(request):
    src.SingleTK.timekeeper().update()
    transactions = TransactionModel.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions})


def index(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def home(request):
    return render(request, 'home.html')


def signup_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.personmodel.name = form.cleaned_data.get('name')
        user.personmodel.surname = form.cleaned_data.get('surname')
        user.personmodel.address = form.cleaned_data.get('address')
        user.personmodel.passport = form.cleaned_data.get('passport')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = RegisterForm(request.POST)
    return render(request, 'registration/register.html', {'form': form})


def put_into_account(request):
    form = PutForm(request.POST)
    if form.is_valid():
        bank_id = int(form.cleaned_data.get("bank_id"))
        account_id = int(form.cleaned_data.get("account_id"))
        summ = int(form.cleaned_data.get("sum"))
        bank = src.SingleDO.DO().get(bank_id, "Bank")
        bank.put(account_id, summ)
        src.SingleDO.DO().done_with(bank_id, "Bank")
        return redirect('home')
    else:
        form = PutForm(request.POST)
    return render(request, 'put_into_account.html', {'form': form})

def get_from_account(request):
    form = PutForm(request.POST)
    if form.is_valid():
        bank_id = int(form.cleaned_data.get("bank_id"))
        account_id = int(form.cleaned_data.get("account_id"))
        summ = int(form.cleaned_data.get("sum"))
        bank = src.SingleDO.DO().get(bank_id, "Bank")
        bank.get(account_id, summ)
        src.SingleDO.DO().done_with(bank_id, "Bank")
        return redirect('home')
    else:
        form = PutForm(request.POST)
    return render(request, 'get_from_account.html', {'form': form})

def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        bank_id = int(form.cleaned_data.get("bank_id"))
        account_id1 = int(form.cleaned_data.get("account_id1"))
        account_id2 = int(form.cleaned_data.get("account_id2"))
        summ = int(form.cleaned_data.get("sum"))
        bank = src.SingleDO.DO().get(bank_id, "Bank")
        bank.transfer(account_id1, account_id2, summ)
        src.SingleDO.DO().done_with(bank_id, "Bank")
        return redirect('home')
    else:
        form = TransferForm(request.POST)
    return render(request, 'transfer.html', {'form': form})
