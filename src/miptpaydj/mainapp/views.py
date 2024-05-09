from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from src.miptpaydj.mainapp.forms import MessengerForm, RegisterForm, PutForm, TransferForm, UpdateProfileForm, CreateClientForm, CreateAccountForm, CreateBankForm, DebitForm, CreditForm, DepositForm
from src.miptpaydj.mainapp.models import BankModel, AccountModel, PlanModel, PersonModel, ConversationModel, MessageModel, ClientModel, TransactionModel

import src


@login_required
def banks(request):
    src.SingleTK.timekeeper().update()
    banks = BankModel.objects.all()
    plans = PlanModel.objects.all()
    plans = [(plan,
              src.Plan.display_commission(plan.commission, plan.increased_commission),
              src.Plan.display_period(plan.period, plan.decreased_period),
              src.Plan.display_limit(plan.lower_limit, plan.decreased_lower_limit))
             for plan in plans]
    form0 = CreateBankForm(request.POST)
    if form0.is_valid():
        bank = str(form0.cleaned_data['bank'])
        src.Bank(None, bank)
        return redirect('/banks/')
    return render(request, 'banks.html', {'banks': banks, 'is_staff': request.user.is_staff, 'plans': plans})


@login_required
def create_plan(request):
    type = request.GET.get('type')
    if type == '0':
        form = DebitForm(request.POST)
        if form.is_valid():
            bank_id = int(form.cleaned_data.get('bank'))
            bank = src.SingleDO.DO().get(bank_id, "Bank")
            if bank is not None:
                debit = src.PlanFactory.create_debit_plan(src.TransferLimit(int(form.cleaned_data.get('transfer_limit')), int(form.cleaned_data.get('decreased_transfer_limit'))), bank_id)
                bank.add_plan(debit.id)
                src.SingleDO.DO().done_with(bank_id, "Bank")
                return redirect(f'/banks/')
    elif type == '1':
        form = CreditForm(request.POST)
        if form.is_valid():
            bank_id = int(form.cleaned_data.get('bank'))
            bank = src.SingleDO.DO().get(bank_id, "Bank")
            if bank is not None:
                credit = src.PlanFactory.create_credit_plan(
                    src.TransferLimit(
                        int(form.cleaned_data.get('transfer_limit')),
                        int(form.cleaned_data.get('decreased_transfer_limit'))
                    ),
                    src.LowerLimit(
                        int(form.cleaned_data.get('lower_limit')),
                        int(form.cleaned_data.get('decreased_lower_limit'))
                    ),
                    src.Commission(
                        float(form.cleaned_data.get('commission')),
                        float(form.cleaned_data.get('decreased_commission'))
                    ),
                    bank_id)
                bank.add_plan(credit.id)
                src.SingleDO.DO().done_with(bank_id, "Bank")
                return redirect(f'/banks/')
    else:
        form = DepositForm(request.POST)
        if form.is_valid():
            bank_id = int(form.cleaned_data.get('bank'))
            bank = src.SingleDO.DO().get(bank_id, "Bank")
            if bank is not None:
                deposit = src.PlanFactory.create_deposit_plan(
                    src.TransferLimit(
                        int(form.cleaned_data.get('transfer_limit')),
                        int(form.cleaned_data.get('decreased_transfer_limit'))
                    ),
                    src.Period(
                        int(form.cleaned_data.get('period')),
                        int(form.cleaned_data.get('decreased_period'))
                    ),
                    src.Commission(
                        float(form.cleaned_data.get('commission')),
                        float(form.cleaned_data.get('decreased_commission'))
                    ),
                    bank_id)
                bank.add_plan(deposit.id)
                src.SingleDO.DO().done_with(bank_id, "Bank")
                return redirect(f'/banks/')
    return render(request, 'create_plan.html', {'type': type})


@login_required
def chats(request):
    src.SingleTK.timekeeper().update()
    current_user = request.user
    current_person = PersonModel.objects.get(user=current_user)
    if current_person.name is None:
        current_person.name = current_user.username
        current_person.save()
    me = PersonModel.objects.get(name="Artem")

    conversations = ConversationModel.objects.filter(senders__id=me.id)

    param = request.GET.get('conversation')
    if param and str(param).isdigit() and 0 <= int(str(param)) < len(conversations):
        current = int(str(param))
        print(current)
        other = conversations[current].senders.all()[1] if conversations[current].senders.all()[0] == me else conversations[current].senders.all()[0]
        messages = reversed(MessageModel.objects.filter(conversation=conversations[current]))
    else:
        current = None
        other = None
        messages = []

    form = MessengerForm(request.POST)
    if current is not None and form.is_valid():
        print("Form is valid")
        text = str(form.cleaned_data.get('text'))
        print(text)
        chat = str(form.cleaned_data.get('chat'))
        print(chat)

        if len(text) > 0:
            src.SingleMB.MB().reset(conversations[current].id, me.id)
            src.SingleMB.MB().fill(text)
            message = src.SingleMB.MB().get()
            src.SingleDO.DO().done_with(message.id, "Message")

            response = redirect(f'/chats/?conversation={current}')
            return response
        elif len(chat) > 0:
            print("Trying to change chat")
            new_other = PersonModel.objects.filter(name=chat)
            if new_other is not None and len(new_other) > 0:
                new_other = new_other[0]
                new_conversation = None
                for c in range(len(conversations)):
                    if new_other in conversations[c].senders.all():
                        new_conversation = c
                        break
                if new_conversation is not None:
                    response = redirect(f'/chats/?conversation={new_conversation}')
                else:
                    src.Conversation(None, [me.id, new_other.id])
                    response = redirect('/chats/?conversation=0')
            else:
                response = redirect(f'/chats/?conversation={current}')
            return response

    discussions = []
    for c in range(len(conversations)):
        conv = conversations[c]
        sender = conv.senders.all()[1] if conv.senders.all()[0] == me else conv.senders.all()[0]
        all_messages = MessageModel.objects.filter(conversation=conv)
        if len(all_messages) > 0:
            last = all_messages[0]
        else:
            last = None
        discussions.append([sender, last, False, c])

    if current is not None:
        discussions[current][2] = True

    return render(request, 'chats.html', {'messages': messages, 'me': me, 'discussions': discussions, 'other': other, 'is_staff': request.user.is_staff})

@login_required
def accounts(request):
    src.SingleTK.timekeeper().update()
    accounts = AccountModel.objects.all()
    current_user = request.user
    current_person = PersonModel.objects.get(user=current_user)
    accounts = [(account, src.Account.display_date(account.freeze_date)) for account in accounts if account.owner.person == current_person or request.user.is_staff]
    form = CreateAccountForm(request.POST)
    if form.is_valid():
        bank_id = int(form.cleaned_data.get('bank'))
        plan_id = int(form.cleaned_data.get('plan'))
        client_id = int(form.cleaned_data.get('client'))
        bank = src.SingleDO.DO().get(bank_id, "Bank")
        if bank is not None:
            bank.open_account(client_id, plan_id)
            src.SingleDO.DO().done_with(bank_id, "Bank")
            return redirect(f'/account/')
    return render(request, 'accounts.html', {'accounts': accounts, 'is_staff': request.user.is_staff})


@login_required
def plans(request):
    src.SingleTK.timekeeper().update()
    plans = PlanModel.objects.all()
    plans = [(plan,
              src.Plan.display_commission(plan.commission, plan.increased_commission),
              src.Plan.display_period(plan.period, plan.decreased_period),
              src.Plan.display_limit(plan.lower_limit, plan.decreased_lower_limit))
             for plan in plans]

    return render(request, 'plans.html', {'plans': plans, 'is_staff': request.user.is_staff})


@login_required
def persons(request):
    src.SingleTK.timekeeper().update()
    persons = PersonModel.objects.all()
    return render(request, 'persons.html', {'persons': persons, 'is_staff': request.user.is_staff})


@login_required
def clients(request):
    src.SingleTK.timekeeper().update()
    clients = ClientModel.objects.all()
    current_user = request.user
    current_person = PersonModel.objects.get(user=current_user)
    clients = [client for client in clients if client.person == current_person or request.user.is_staff]
    form = CreateClientForm(request.POST)
    if form.is_valid():
        print("Valid form")
        bank_id = int(form.cleaned_data.get('bank'))
        bank = src.SingleDO.DO().get(bank_id, "Bank")
        if bank is not None:
            i = bank.register(current_person.name, current_person.surname, "NO_VALUE", "NO_VALUE", current_person.id)
            print("Client's ID is", i)
            src.SingleDO.DO().done_with(bank_id, "Bank")
            return redirect(f'/clients/')
    return render(request, 'clients.html', {'clients': clients, 'is_staff': request.user.is_staff})


@login_required
def transactions(request):
    src.SingleTK.timekeeper().update()
    transactions = TransactionModel.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions, 'is_staff': request.user.is_staff})


def index(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def home(request):
    current_user = request.user
    current_person = PersonModel.objects.get(user=current_user)
    form = UpdateProfileForm(request.POST)
    if form.is_valid():
        current_user = request.user
        current_person = PersonModel.objects.get(user=current_user)
        current_person.name = str(form.cleaned_data.get("name"))
        current_person.surname = str(form.cleaned_data.get("surname"))
        current_person.address = str(form.cleaned_data.get("address"))
        current_person.passport = str(form.cleaned_data.get("passport"))
        current_person.save()
    return render(request, 'home.html', {'current_person': current_person, 'is_staff': request.user.is_staff})


@login_required
def put(request):
    form = PutForm(request.POST)
    if form.is_valid():
        bank_id = int(form.cleaned_data.get("bank_id"))
        account_id = int(form.cleaned_data.get("account_id"))
        amount = float(form.cleaned_data.get("amount"))

        bank = src.SingleDO.DO().get(bank_id, "Bank")
        if bank is not None:
            bank.put(account_id, amount)
        src.SingleDO.DO().done_with(bank_id, "Bank")

        return redirect('home')
    else:
        form = PutForm(request.POST)
    return render(request, 'material_put.html', {'form': form, 'is_staff': request.user.is_staff})


@login_required
def get(request):
    form = PutForm(request.POST)
    if form.is_valid():
        bank_id = int(form.cleaned_data.get("bank_id"))
        account_id = int(form.cleaned_data.get("account_id"))
        amount = float(form.cleaned_data.get("amount"))

        bank = src.SingleDO.DO().get(bank_id, "Bank")
        if bank is not None:
            bank.get(account_id, amount)
        src.SingleDO.DO().done_with(bank_id, "Bank")
        return redirect('home')
    else:
        form = PutForm(request.POST)
    return render(request, 'material_get.html', {'form': form, 'is_staff': request.user.is_staff})


@login_required
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        departure_bank = int(form.cleaned_data.get("departure_bank"))
        departure_account = int(form.cleaned_data.get("departure_account"))
        destination_bank = int(form.cleaned_data.get("destination_bank"))
        destination_account = int(form.cleaned_data.get("destination_account"))
        amount = float(form.cleaned_data.get("amount"))

        if departure_bank == destination_bank:
            bank = src.SingleDO.DO().get(departure_bank, "Bank")
            if bank is not None:
                bank.transfer(departure_account, destination_account, amount)
            src.SingleDO.DO().done_with(departure_bank, "Bank")
        else:
            src.SingleSPF.CPF().transfer(departure_bank, departure_account, destination_bank, destination_account, amount)

        return redirect('home')
    else:
        form = TransferForm(request.POST)
    return render(request, 'material_transfer.html', {'form': form, 'is_staff': request.user.is_staff})


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
    return render(request, 'registration/register.html', {'form': form, 'is_staff': request.user.is_staff})
