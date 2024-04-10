from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from src.miptpaydj.mainapp.forms import RegisterForm
from src.miptpaydj.mainapp.models import BankModel, AccountModel, PlanModel, PersonModel, ClientModel, TransactionModel
import src


def banks(request):
    banks = BankModel.objects.all()
    return render(request, 'banks.html', {'banks': banks})


def accounts(request):
    # tst = src.AccountModel.objects.get(id=1)
    # bnk = src.BankModel.objects.get(id=3)

    # tst = src.DataOperator().get(1, "Account")
    bank = src.DataOperator().get(3, "Bank")
    bank.put(12, 100)
    src.DataOperator().done_with(3, "Bank")

    accounts = AccountModel.objects.all()
    return render(request, 'accounts.html', {'accounts': accounts})


def plans(request):
    plans = PlanModel.objects.all()
    return render(request, 'plans.html', {'plans': plans})


def persons(request):
    persons = PersonModel.objects.all()
    return render(request, 'persons.html', {'persons': persons})


def clients(request):
    bank = src.DataOperator().get(3, "Bank")
    bank.update(2, "kalinin.mi@phystech.edu", "1000 000000")
    src.DataOperator().done_with(3, "Bank")

    clients = ClientModel.objects.all()
    clnt = ClientModel.objects.get(id=2)
    print(clnt.passport)
    return render(request, 'clients.html', {'clients': clients})


def transactions(request):
    transactions = TransactionModel.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions})


def hello_world(request):
    return render(request, 'index.html', {'greeting': 'Hello, world!'})


@login_required
def profile(request):
    return render(request, 'profile.html')

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
