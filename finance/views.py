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

    debt_sum = 0
    wallet_cash = 0
    for order in orders:
        if order.payment_status == 'not paid':
            debt_sum += order.total_sum
        else:
            wallet_cash += order.total_sum

    wallet = wallet.last()
    debt = debt.last()

    wallet.cash = wallet_cash
    wallet.save()
    debt.debt = debt_sum
    debt.save()



    context = {
        'wallet': wallet,
        'debt': debt
    }

    return render(request, 'finance/finance.html', context)
