from django import forms
from .models import Customer, Order, Accessories
from settings.models import PriceAccessories

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('full_name', 'phone_number',)
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Фамилия Имя Отчество'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '8(9XX)XXX XX XX'
            })
        }

class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer', 'width', 'length', 'fabric_size',
                  'payment_status', 'ceiling_type', 'photo', 'status')
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'required': True

            }),
            'width': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'В метрах'
            }),
            'length': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'В метрах'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'form-select',
               # 'placeholder': 'Сумма предоплаты'
            }),
            'fabric_size': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ceiling_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, user, *args, **kwargs):
        # Фильтрация клиентов по текущему пользователю
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(user=user)


class CustomerSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        label='Поиск клиента',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя или телефон...',
            'class': 'form-control',
            'autocomplete': 'off'
        })
    )

class AccessoriesForm(forms.ModelForm):
    class Meta:
        model = Accessories
        fields = ('customer', 'accessories', 'quantity')
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'accessories': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'placeholder': 'Количество'
            })
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтрация клиентов по текущему пользователю
        self.fields['customer'].queryset = Customer.objects.filter(user=user)
        self.fields['accessories'].queryset = PriceAccessories.objects.filter(user=user)
