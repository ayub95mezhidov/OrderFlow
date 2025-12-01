from decimal import Decimal

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView
from django.utils import timezone
from django.db.models import Sum

from calendar import monthrange
from datetime import timedelta
import json

from .forms import WalletForm, DebtForm, IncomeForm, ExpensesForm, CategoryIncomeForm, CategoryExpensesForm
from .models import Wallet, Debt, Income, Expenses, CategoryIncome, CategoryExpenses, Profit

@login_required(login_url='/users/login/')
def finance(request):
    period = request.GET.get("period", "day")   # day / week / month
    offset = int(request.GET.get("offset", "0"))

    # Получает или создает запись кошелька и долга для текушего пользователя
    Wallet.objects.get_or_create(user=request.user)
    Debt.objects.get_or_create(user=request.user)

    today = timezone.now().date()

    incomes_grouped = []
    expenses_grouped = []
    income_labels = []
    income_values = []
    expense_labels = []
    expense_values = []

    COLOR_MAP = {
        "Красный": "#f44336",
        "Синий": "#2196f3",
        "Зеленый": "#4caf50",
        "Желтый": "#ffeb3b",
        "Оранжевый": "#ff9800",
        "Фиолетовый": "#9c27b0",
        "Розовый": "#e91e63",
        "Коричневый": "#795548",
        "Черный": "#000000",
        "Белый": "#ffffff",
        "Серый": "#9e9e9e",
    }

    # ---------- ДЕНЬ ----------
    if period == "day":
        target_day = today + timedelta(days=offset)
        incomes = Income.objects.filter(user=request.user, date__date=target_day)
        expenses = Expenses.objects.filter(user=request.user, date__date=target_day)

        # Если по этой дате нету записи, создаем новый
        try:
            profit = Profit.objects.filter(user=request.user, date__date=target_day).last()
            total_profit = profit.total
        except Exception as ex:
            profit = Profit.objects.create(user=request.user, total=Decimal(0), date=target_day)
            total_profit = profit.total


        # Группировка доходов по категориям
        incomes_grouped = (
            incomes.values("title__title", "title__color")
            .annotate(total=Sum("total_sum"))
            .order_by("title__title")
        )

        # Группировка расходов по категориям
        expenses_grouped = (
            expenses.values("title__title", "title__color")
            .annotate(total=Sum("total_sum"))
            .order_by("title__title")
        )

        # Данные для графиков
        income_labels = json.dumps([i["title__title"] for i in incomes_grouped])
        income_values = json.dumps([float(i["total"]) for i in incomes_grouped])
        income_colors = json.dumps([COLOR_MAP[i["title__color"]] for i in incomes_grouped])

        expense_labels = json.dumps([i["title__title"] for i in expenses_grouped])
        expense_values = json.dumps([float(i["total"]) for i in expenses_grouped])
        expense_colors = json.dumps([COLOR_MAP[e["title__color"]] for e in expenses_grouped])

        period_title = target_day.strftime("%d.%m.%Y")

    # ---------- НЕДЕЛЯ ----------
    elif period == "week":
        weekday = today.weekday()
        monday = today - timedelta(days=weekday)
        monday = monday + timedelta(weeks=offset)
        sunday = monday + timedelta(days=6)

        incomes = Income.objects.filter(user=request.user, date__date__range=[monday, sunday])
        expenses = Expenses.objects.filter(user=request.user, date__date__range=[monday, sunday])
        profit = Profit.objects.filter(user=request.user, date__date__range=[monday, sunday])

        total_profit = 0
        for obj in profit:
            total_profit += obj.total

        # Группировка доходов по категориям
        incomes_grouped = (
            incomes.values("title__title", "title__color")
            .annotate(total=Sum("total_sum"))
            .order_by("title__title")
        )

        # Группировка расходов по категориям
        expenses_grouped = (
            expenses.values("title__title", "title__color")
            .annotate(total=Sum("total_sum"))
            .order_by("title__title")
        )

        # Данные для графиков
        income_labels = json.dumps([i["title__title"] for i in incomes_grouped])
        income_values = json.dumps([float(i["total"]) for i in incomes_grouped])
        income_colors = json.dumps([COLOR_MAP[i["title__color"]] for i in incomes_grouped])

        expense_labels = json.dumps([i["title__title"] for i in expenses_grouped])
        expense_values = json.dumps([float(i["total"]) for i in expenses_grouped])
        expense_colors = json.dumps([COLOR_MAP[e["title__color"]] for e in expenses_grouped])

        period_title = f"{monday.strftime('%d.%m')} — {sunday.strftime('%d.%m')}"

    # ---------- МЕСЯЦ ----------
    else:  # period == "month"
        year = today.year
        month = today.month + offset

        # Выходим за границы: декабрь → январь
        while month > 12:
            month -= 12
            year += 1
        while month < 1:
            month += 12
            year -= 1

        first_day = timezone.datetime(year, month, 1).date()
        last_day = timezone.datetime(year, month, monthrange(year, month)[1]).date()

        period_title = f"{first_day.strftime('%B %Y')}"

        incomes = Income.objects.filter(user=request.user, date__date__range=[first_day, last_day])
        expenses = Expenses.objects.filter(user=request.user, date__date__range=[first_day, last_day])
        profit = Profit.objects.filter(user=request.user, date__date__range=[first_day, last_day])

        total_profit = 0
        for obj in profit:
            total_profit += obj.total

        # Группировка доходов по категориям
        incomes_grouped = (
            incomes.values("title__title", "title__color")
            .annotate(total=Sum("total_sum"))
            .order_by("title__title")
        )

        # Группировка расходов по категориям
        expenses_grouped = (
            expenses.values("title__title", "title__color")
            .annotate(total=Sum("total_sum"))
            .order_by("title__title")
        )

        # Данные для графиков
        income_labels = json.dumps([i["title__title"] for i in incomes_grouped])
        income_values = json.dumps([float(i["total"]) for i in incomes_grouped])
        income_colors = json.dumps([COLOR_MAP[i["title__color"]] for i in incomes_grouped])

        expense_labels = json.dumps([i["title__title"] for i in expenses_grouped])
        expense_values = json.dumps([float(i["total"]) for i in expenses_grouped])
        expense_colors = json.dumps([COLOR_MAP[e["title__color"]] for e in expenses_grouped])


    # Итоги
    total_income = incomes.aggregate(Sum("total_sum"))["total_sum__sum"] or 0
    total_expenses = expenses.aggregate(Sum("total_sum"))["total_sum__sum"] or 0
    balance = total_income - total_expenses



    context = {
        'wallet': Wallet.objects.filter(user=request.user).last(),
        'debt': Debt.objects.filter(user=request.user).last(),
        "total_profit": total_profit,
        "period": period,
        "offset": offset,
        "period_title": period_title,
        "incomes_grouped": incomes_grouped,
        "expenses_grouped": expenses_grouped,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "income_labels": income_labels,
        "income_values": income_values,
        "expense_labels": expense_labels,
        "expense_values": expense_values,
        "income_colors": income_colors,
        "expense_colors": expense_colors,
    }

    return render(request, "finance/finance.html", context)


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

    def get_form_kwargs(self):
        """Передаем пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

    def get_form_kwargs(self):
        """Передаем пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.date = timezone.now().date()
        self.object.save()

        # Обновляем кошелек
        try:
            wallet = Wallet.objects.filter(user=self.request.user).last()
            if wallet:
                wallet.cash -= self.object.total_sum
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
    
class CategoryIncomeCreateView(CreateView, LoginRequiredMixin):
    login_url = '/users/login/'
    model = CategoryIncome
    form_class = CategoryIncomeForm
    template_name = 'finance/create_category_income.html'
    success_url = reverse_lazy('create_income')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        
        return super().form_valid(form)


class CategoryExpensesCreateView(CreateView, LoginRequiredMixin):
    login_url = '/users/login/'
    model = CategoryExpenses
    form_class = CategoryExpensesForm
    template_name = 'finance/create_category_expenses.html'
    success_url = reverse_lazy('create_expenses')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        return super().form_valid(form)




