from django.shortcuts import render

from .models import Wallet, Debt

def finance(request):
    return render(request, 'finance/finance.html')
