from django import forms

from .models import Wallet, Debt, Income, Expenses, NameIncome, NameExpenses

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

class NameIncomeForm(forms.ModelForm):
    class Meta:
        model = NameIncome
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

class NameExpensesForm(forms.ModelForm):
    class Meta:
        model = NameExpenses
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