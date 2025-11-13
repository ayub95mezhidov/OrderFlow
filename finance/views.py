from django.shortcuts import render

from .models import Wallet, Debt
from orders.models import Order, Accessories

def finance(request):
    wallet = Wallet.objects.filter(user=request.user)
    debt = Debt.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)

    # Проверяет и создает новый объект
    if len(wallet) == 0 and len(debt) == 0 :
        wallet = Wallet.objects.create(user=request.user)
        debt = Debt.objects.create(user=request.user)


    wallet = wallet.last()
    debt = debt.last()


    context = {
        'wallet': wallet,
        'debt': debt
    }

    return render(request, 'finance/finance.html', context)
