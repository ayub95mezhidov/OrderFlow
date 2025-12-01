from django import forms

from .models import Wallet, Debt, Income, Expenses, CategoryIncome, CategoryExpenses

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ('cash',)
        widgets = {
            'cash': forms.NumberInput(attrs={
                'class': 'form-control',
            })
        }

class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ('debt',)
        widgets = {
            'debt': forms.NumberInput(attrs={
                'class': 'form-control',
            })
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('total_sum', 'title')
        widgets = {
            'total_sum': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'title': forms.Select(attrs={
                'class': 'form-select',
               # 'placeholder': ''
            })
        }
    def __init__(self, user, *args, **kwargs):
        # Фильтрация катигории по текущему пользователю
        super().__init__(*args, **kwargs)
        self.fields['title'].queryset = CategoryIncome.objects.filter(user=user)

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ('total_sum', 'title')
        widgets = {
            'total_sum': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'title': forms.Select(attrs={
                'class': 'form-select',
               # 'placeholder': ''
            })
        }

    def __init__(self, user, *args, **kwargs):
        # Фильтрация катигории по текущему пользователю
        super().__init__(*args, **kwargs)
        self.fields['title'].queryset = CategoryExpenses.objects.filter(user=user)

class CategoryIncomeForm(forms.ModelForm):
    class Meta:
        model = CategoryIncome
        fields = ('title', 'color')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            'color': forms.Select(attrs={
                'class': 'form-select',
            })
        }

class CategoryExpensesForm(forms.ModelForm):
    class Meta:
        model = CategoryExpenses
        fields = ('title', 'color')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            'color': forms.Select(attrs={
                'class': 'form-select',
            })
        }