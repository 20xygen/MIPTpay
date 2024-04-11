from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.accounts, name='accounts'),
    path('banks/', views.banks, name='banks'),
    path('plans/', views.plans, name='plans'),
    path('persons/', views.persons, name='persons'),
    path('clients/', views.clients, name='clients'),
    path('transactions/', views.transactions, name='transactions'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.signup_view, name='register'),
    path('home/', views.home, name='home')
]