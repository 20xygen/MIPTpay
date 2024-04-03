from django.contrib import admin
from .models import Bank, Person, Client, PlanCategory, Plan, Account, Transaction, Diary

admin.site.register(Bank)
admin.site.register(Person)
admin.site.register(Client)
admin.site.register(PlanCategory)
admin.site.register(Plan)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Diary)
