from django import forms
from .models import PriceSettings, PriceAccessories

class PriceSettingsForms(forms.ModelForm):
    class Meta:
        model = PriceSettings
        fields = ('fabric_size', 'ceiling_type', 'bought', 'markup')
        widgets = {
            'fabric_size': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'ceiling_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'bought': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Купил за м²'
            }),
            'markup': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Наценка за м²'
            }),
        }

class PriceAccessoriesForm(forms.ModelForm):
    class Meta:
        model = PriceAccessories
        fields = ('accessories', 'bought', 'markup')
        widgets = {
            'accessories': forms.TextInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Введите название комплектующего'
            }),
            'bought': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Купил за'
            }),
            'markup': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Купил за'
            }),
        }