from django.contrib import admin

from .models import Wallet, Debt, CategoryIncome, CategoryExpenses, Income, Expenses, Profit

admin.site.register(Wallet)
admin.site.register(Debt)
admin.site.register(CategoryIncome)
admin.site.register(CategoryExpenses)
admin.site.register(Income)
admin.site.register(Expenses)
admin.site.register(Profit)
