from django.contrib import admin
from .models import PriceSettings, PriceAccessories

admin.site.register(PriceSettings)
admin.site.register(PriceAccessories)