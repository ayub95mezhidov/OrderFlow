from django.contrib import admin
from .models import DailyStats, MonthlyStats, GoalSettings

admin.site.register(DailyStats)
admin.site.register(MonthlyStats)
admin.site.register(GoalSettings)