from django.contrib import admin
from django.urls import path

from .views import finance, WalletUpdateView, DebtUpdateView, IncomeCreateView, ExpensesCreateView

urlpatterns = [
    path('finance/', finance, name='finance'),
    path('finance/update_wallet', WalletUpdateView.as_view(), name='update_wallet'),
    path('finance/update_debt', DebtUpdateView.as_view(), name='update_debt'),
    path('finance/create_income', IncomeCreateView.as_view(), name='create_income'),
    path('finance/create_expenses', ExpensesCreateView.as_view(), name='create_expenses'),

]