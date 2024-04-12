from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, help_text='Name')
    surname = forms.CharField(max_length=100, help_text='Surname')
    address = forms.CharField(max_length=150, help_text='Address')
    passport = forms.IntegerField(help_text='Passport')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'surname', 'address', 'passport')

class PutForm(forms.Form):
    bank_id = forms.CharField(max_length=100, help_text='Bank ID')
    account_id = forms.CharField(max_length=100, help_text='Account ID')
    sum = forms.CharField(max_length=150, help_text='Sum')

class TransferForm(forms.Form):
    bank_id = forms.CharField(max_length=100, help_text='Bank ID')
    account_id1 = forms.CharField(max_length=100, help_text='Account ID1')
    account_id2 = forms.CharField(max_length=100, help_text='Account ID2')
    sum = forms.CharField(max_length=150, help_text='Sum')
