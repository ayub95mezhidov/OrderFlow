from django.contrib import admin
from django.urls import path

from .views import finance, WalletUpdateView, DebtUpdateView, IncomeCreateView, ExpensesCreateView, CategoryIncomeCreateView, CategoryExpensesCreateView

urlpatterns = [
    path('', finance, name='finance'),
    path('update_wallet/', WalletUpdateView.as_view(), name='update_wallet'),
    path('update_debt/', DebtUpdateView.as_view(), name='update_debt'),
    path('create_income/', IncomeCreateView.as_view(), name='create_income'),
    path('create_expenses/', ExpensesCreateView.as_view(), name='create_expenses'),
    path('create_category_income/', CategoryIncomeCreateView.as_view(), name='create_category_income'),
    path('create_category_expenses/', CategoryExpensesCreateView.as_view(), name='create_category_expenses'),

]