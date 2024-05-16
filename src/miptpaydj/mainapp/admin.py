from django.contrib import admin
from .models import BankModel, PersonModel, ConversationModel, MessageModel, ClientModel, PlanCategoryModel, PlanModel, AccountModel, TransactionModel, DiaryModel

admin.site.register(BankModel)
admin.site.register(PersonModel)
admin.site.register(ConversationModel)
admin.site.register(MessageModel)
admin.site.register(ClientModel)
admin.site.register(PlanCategoryModel)
admin.site.register(PlanModel)
admin.site.register(AccountModel)
admin.site.register(TransactionModel)
admin.site.register(DiaryModel)

class PersonInline(admin.StackedInline):
    model = PersonModel
    can_delete = False
    verbose_name_plural = 'person'
