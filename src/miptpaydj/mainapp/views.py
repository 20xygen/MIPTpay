from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from src.miptpaydj.mainapp.forms import RegisterForm
from src.miptpaydj.mainapp.models import BankModel, AccountModel, PlanModel, PersonModel, ClientModel, TransactionModel

import src

def banks(request):
    src.SingleTK.timekeeper().update()
    banks = BankModel.objects.all()
    return render(request, 'banks.html', {'banks': banks})


def accounts(request):
    src.SingleTK.timekeeper().update()

    # bank = src.SingleDO.DO().get(1, "Bank")
    # bank.put(3, 100)
    # src.SingleDO.DO().done_with(1, "Bank")
    #
    # bank = src.SingleDO.DO().get(2, "Bank")
    # bank.get(6, 1000)
    # src.SingleDO.DO().done_with(2, "Bank")

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
