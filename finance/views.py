from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView
from django.utils import timezone

from .forms import WalletForm, DebtForm, IncomeForm, ExpensesForm
from .models import Wallet, Debt, Income, Expenses
from orders.models import Order, Accessories

def finance(request):
    # Получает или создает запись кошелька и долга для текушего пользователя
    Wallet.objects.get_or_create(user=request.user)
    Debt.objects.get_or_create(user=request.user)

    income = Income.objects.filter(user=request.user)
    expenses = Expenses.objects.filter(user=request.user)

    context = {
        'wallet': Wallet.objects.filter(user=request.user).last(),
        'debt': Debt.objects.filter(user=request.user).last(),
        'income': income,
        'expenses': expenses
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

class IncomeCreateView(CreateView, LoginRequiredMixin):
    login_url = '/users/login/'
    model = Income
    form_class = IncomeForm
    template_name = 'finance/create_income.html'
    success_url = reverse_lazy('finance')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.date = timezone.now().date()
        self.object.save()

        # Обновляем кошелек
        try:
            wallet = Wallet.objects.filter(user=self.request.user).last()
            if wallet:
                wallet.cash += self.object.total_sum
                wallet.save()
            else:
                # Если кошелка нет, можно создать новый
                Wallet.objects.create(
                    user=self.request.user,
                    cash=self.object.total_sum
                )
        except Exception as ex:
            print(ex)

        return super().form_valid(form)

class ExpensesCreateView(CreateView, LoginRequiredMixin):
    login_url = '/users/login/'
    model = Income
    form_class = ExpensesForm
    template_name = 'finance/create_expenses.html'
    success_url = reverse_lazy('finance')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.date = timezone.now().date()
        self.object.save()

        # Обновляем счетчик долга
        try:
            debt = Debt.objects.filter(user=self.request.user).last()
            if debt:
                debt.debt += self.object.total_sum
                debt.save()
            else:
                # Если счетчик долга нет, можно создать новый
                Debt.objects.create(
                    user=self.request.user,
                    debt=self.object.total_sum
                )
        except Exception as ex:
            print(ex)

        return super().form_valid(form)

