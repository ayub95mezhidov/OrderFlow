from django import forms
from django.forms import ModelForm

from .models import GoalSettings

class GoalForm(forms.ModelForm):
    class Meta:
        model = GoalSettings
        fields = ('daily_goal', 'monthly_goal')
        widgets = {
            'daily_goal': forms.NumberInput(attrs={
                'class': 'form-control',
                #'placeholder': ''
            }),
            'monthly_goal': forms.NumberInput(attrs={
                'class': 'form-control',
            })
        }
