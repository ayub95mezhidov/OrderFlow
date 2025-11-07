from django import forms
from .models import PriceSettings, PriceAccessories

class PriceSettingsForms(forms.ModelForm):
    class Meta:
        model = PriceSettings
        fields = ('fabric_size', 'ceiling_type', 'price_m2')
        widgets = {
            'fabric_size': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'ceiling_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'price_m2': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Цена за м²'
            })
        }

class PriceAccessoriesForm(forms.ModelForm):
    class Meta:
        model = PriceAccessories
        fields = ('accessories', 'price')
        widgets = {
            'accessories': forms.TextInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Введите название комплектующего'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Цена'
            })
        }