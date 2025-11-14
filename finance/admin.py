from django.contrib import admin

from .models import Wallet, Debt, NameIncome, NameExpenses, Income, Expenses

admin.site.register(Wallet)
admin.site.register(Debt)
admin.site.register(NameIncome)
admin.site.register(NameExpenses)
admin.site.register(Income)
admin.site.register(Expenses)
