from django import forms

from .models import Wallet, Debt

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

