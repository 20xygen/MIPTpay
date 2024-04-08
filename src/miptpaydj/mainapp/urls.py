from django.urls import path, include
from . import views
from .views import RegisterView

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('account/', views.accounts, name='accounts'),
    path('banks/', views.banks, name='banks'),
    path('plans/', views.plans, name='plans'),
    path('persons/', views.persons, name='persons'),
    path('clients/', views.clients, name='clients'),
    path('transactions/', views.transactions, name='transactions'),
    path('profile/', views.profile, name='profile'),
    path('register/', RegisterView.as_view(), name='register')
]
