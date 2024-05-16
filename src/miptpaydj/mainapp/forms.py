from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateBankForm(forms.Form):
    bank = forms.CharField(label='Name', max_length=100)

    class Meta(UserCreationForm.Meta):
        fields = ['bank']


class DebitForm(forms.Form):
    transfer_limit = forms.CharField(label='Transfer Limit', max_length=100)
    decreased_transfer_limit = forms.CharField(label='Decreased Transfer Limit', max_length=100)
    bank = forms.CharField(label='Name', max_length=100)

    class Meta(UserCreationForm.Meta):
        fields = ['transfer_limit', 'decreased_transfer_limit', 'bank']


class CreditForm(forms.Form):
    transfer_limit = forms.CharField(label='Credit Limit', max_length=100)
    decreased_transfer_limit = forms.CharField(label='Decreased Credit Limit', max_length=100)
    lower_limit = forms.CharField(label='Lower Limit', max_length=100)
    decreased_lower_limit = forms.CharField(label='Decreased Lower Limit', max_length=100)
    commission = forms.CharField(label='Commission', max_length=100)
    decreased_commission = forms.CharField(label='Decreased Commission', max_length=100)
    bank = forms.CharField(label='Name', max_length=100)

    class Meta(UserCreationForm.Meta):
        fields = ['transfer_limit', 'decreased_transfer_limit', 'lower_limit', 'decreased_lower_limit', 'commission', 'decreased_commission', 'bank']


class DepositForm(forms.Form):
    transfer_limit = forms.CharField(label='Credit Limit', max_length=100)
    decreased_transfer_limit = forms.CharField(label='Decreased Credit Limit', max_length=100)
    period = forms.CharField(label='Lower Limit', max_length=100)
    decreased_period = forms.CharField(label='Decreased Lower Limit', max_length=100)
    commission = forms.CharField(label='Commission', max_length=100)
    decreased_commission = forms.CharField(label='Decreased Commission', max_length=100)
    bank = forms.CharField(label='Name', max_length=100)

    class Meta(UserCreationForm.Meta):
        fields = ['transfer_limit', 'decreased_transfer_limit', 'period', 'decreased_period', 'commission',
                  'decreased_commission', 'bank']


class CreateClientForm(forms.Form):
    bank = forms.CharField(max_length=100, help_text='Bank ID')

    class Meta(UserCreationForm.Meta):
        fields = ['bank']


class CreateAccountForm(forms.Form):
    bank = forms.CharField(max_length=100, help_text='Bank ID')
    plan = forms.CharField(max_length=100, help_text='Plan ID')
    client = forms.CharField(max_length=100, help_text='Client ID')

    class Meta(UserCreationForm.Meta):
        fields = ['bank', 'plan', 'client']


class UpdateProfileForm(forms.Form):
    name = forms.CharField(max_length=100, help_text='Name', required=False)
    surname = forms.CharField(max_length=100, help_text='Surname', required=False)
    address = forms.CharField(max_length=150, help_text='Address', required=False)
    passport = forms.IntegerField(help_text='Passport', required=False)

    class Meta(UserCreationForm.Meta):
        fields = ['name', 'surname', 'address', 'passport']


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Name')
    surname = forms.CharField(max_length=100, help_text='Surname')
    address = forms.CharField(max_length=150, help_text='Address')
    passport = forms.IntegerField(help_text='Passport')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'surname', 'address', 'passport')

class MessengerForm(forms.Form):
    text = forms.CharField(max_length=500, help_text='Text', required=False)
    chat = forms.CharField(max_length=50, help_text='Chat', required=False)

    class Meta:
        fields = ["text", "chat"]


class PutForm(forms.Form):
    bank_id = forms.CharField(max_length=100, help_text='Bank ID')
    account_id = forms.CharField(max_length=100, help_text='Account ID')
    amount = forms.CharField(max_length=150, help_text='Amount')


class TransferForm(forms.Form):
    departure_bank = forms.CharField(max_length=100, help_text='Bank ID1')
    departure_account = forms.CharField(max_length=100, help_text='Account ID1')
    destination_bank = forms.CharField(max_length=100, help_text='Bank ID2')
    destination_account = forms.CharField(max_length=100, help_text='Account ID2')
    amount = forms.CharField(max_length=150, help_text='Amount')
