from django.core.handlers.exception import response_for_exception
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from .forms import WalletForm, DebtForm
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

class WalletUpdateView(UpdateView, LoginRequiredMixin):
    login_url = '/users/login/'
    model = Wallet
    form_class = WalletForm
    template_name = 'finance/update_wallet.html'
    success_url = reverse_lazy('finance')

    def get_object(self, queryset=None):
        obj, created = Wallet.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        Wallet.objects.filter(user=self.request.user).update(cash=self.object.cash)
        return response

class DebtUpdateView(UpdateView, LoginRequiredMixin):
    login_url = '/users/login/'
    model = Debt
    form_class = DebtForm
    template_name = 'finance/update_debt.html'
    success_url = reverse_lazy('finance')

    def get_object(self, queryset=None):
        obj, created = Debt.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        responce = super().form_valid(form)
        Debt.objects.filter(user=self.request.user).update(debt=self.object.debt)
        return responce

