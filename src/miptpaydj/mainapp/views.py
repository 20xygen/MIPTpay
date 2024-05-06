from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from src.miptpaydj.mainapp.forms import MessageSendForm, RegisterForm, PutForm, TransferForm
from src.miptpaydj.mainapp.models import BankModel, AccountModel, PlanModel, PersonModel, ConversationModel, MessageModel, ClientModel, TransactionModel

import src


def banks(request):
    src.SingleTK.timekeeper().update()

    banks = BankModel.objects.all()
    return render(request, 'banks.html', {'banks': banks})

def chats(request):
    src.SingleTK.timekeeper().update()

    me = PersonModel.objects.get(name="Denis")

    conversations = ConversationModel.objects.filter(senders__id=me.id)

    param = request.GET.get('conversation')
    if param and str(param).isdigit() and 0 <= int(str(param)) < len(conversations):
        current = int(str(param))
        print(current)
        other = conversations[current].senders.all()[1] if conversations[current].senders.all()[0] == me else conversations[current].senders.all()[0]
        messages = reversed(MessageModel.objects.filter(conversation=conversations[current]))

        form = MessageSendForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            print(form.cleaned_data.get('text'))
            text = str(form.cleaned_data.get('text'))

            src.SingleMB.MB().reset(conversations[current].id, me.id)
            src.SingleMB.MB().fill(text)
            message = src.SingleMB.MB().get()
            src.SingleDO.DO().done_with(message.id, "Message")

            response = redirect(f'/chats/?conversation={current}')
            return response
    else:
        current = None
        other = None
        messages = []

    discussions = []
    for c in range(len(conversations)):
        conv = conversations[c]
        sender = conv.senders.all()[1] if conv.senders.all()[0] == me else conv.senders.all()[0]
        last = MessageModel.objects.filter(conversation=conv)[0]
        discussions.append([sender, last, False, c])

    if current is not None:
        discussions[current][2] = True

    return render(request, 'chats.html', {'messages': messages, 'me': me, 'discussions': discussions, 'other': other})

def accounts(request):
    src.SingleTK.timekeeper().update()

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


# @login_required
def home(request):
    return render(request, 'home.html')


# @login_required
def put(request):
    form = PutForm(request.POST)
    if form.is_valid():
        bank_id = int(form.cleaned_data.get("bank_id"))
        account_id = int(form.cleaned_data.get("account_id"))
        amount = int(form.cleaned_data.get("amount"))
        bank = src.SingleDO.DO().get(bank_id, "Bank")
        bank.put(account_id, amount)
        src.SingleDO.DO().done_with(bank_id, "Bank")
        return redirect('home')
    else:
        form = PutForm(request.POST)
    return render(request, 'material_put.html', {'form': form})


# @login_required
def get(request):
    form = PutForm(request.POST)
    if form.is_valid():
        bank_id = int(form.cleaned_data.get("bank_id"))
        account_id = int(form.cleaned_data.get("account_id"))
        amount = int(form.cleaned_data.get("amount"))
        bank = src.SingleDO.DO().get(bank_id, "Bank")
        bank.get(account_id, amount)
        src.SingleDO.DO().done_with(bank_id, "Bank")
        return redirect('home')
    else:
        form = PutForm(request.POST)
    return render(request, 'material_get.html', {'form': form})


# @login_required
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        departure_bank = int(form.cleaned_data.get("departure_bank"))
        departure_account = int(form.cleaned_data.get("departure_account"))
        destination_bank = int(form.cleaned_data.get("destination_bank"))
        destination_account = int(form.cleaned_data.get("destination_account"))
        amount = int(form.cleaned_data.get("amount"))

        if departure_bank == destination_bank:
            bank = src.SingleDO.DO().get(departure_bank, "Bank")
            bank.transfer(departure_account, destination_account, amount)
            src.SingleDO.DO().done_with(departure_bank, "Bank")
        else:
            src.SingleSPF.CPF().transfer(departure_bank, departure_account, destination_bank, destination_account, amount)

        return redirect('home')
    else:
        form = TransferForm(request.POST)
    return render(request, 'material_transfer.html', {'form': form})


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
