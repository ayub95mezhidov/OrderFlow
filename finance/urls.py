from django.contrib import admin
from django.urls import path

from .views import finance, WalletUpdateView, DebtUpdateView

urlpatterns = [
    path('finance/', finance, name='finance'),
    path('finance/update_wallet', WalletUpdateView.as_view(), name='update_wallet'),
    path('finance/update_debt', DebtUpdateView.as_view(), name='update_debt'),
]