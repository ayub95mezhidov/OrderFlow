from django.db import models
from django.db.models import CASCADE, ForeignKey
from django.utils import timezone
from decimal import Decimal
import calendar

from users.models import User


class GoalSettings(models.Model):
    daily_goal = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_goal = models.DecimalField(max_digits=10, decimal_places=2)
    user = ForeignKey(to=User, on_delete=CASCADE)

    class Meta:
        verbose_name = "Настройка цели"
        verbose_name_plural = "Настройка цели"
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_goal')
        ]

    def __str__(self):
        return f' {self.user} - Дневная цель: {self.daily_goal}кв Месячная цель: {self.monthly_goal}кв'

class DailyStats(models.Model):
    date = models.DateTimeField(default=timezone.now)
    completed_m2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    count_completed_orders = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    daily_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = ForeignKey(to=User, on_delete=CASCADE)

    class Meta:
        verbose_name = "Дневная статистика"
        verbose_name_plural = "Дневная статистика"

    def __str__(self):
        return f"{self.user} - Статистика за {self.date.strftime('%d.%m.%Y')}"

    @property
    def progress_percentage(self):
        """Вычесляет сколько прецентов осталось до цели"""
        if self.daily_goal == 0:
            return 0
        return min(100, int((self.completed_m2 / self.daily_goal) * 100))

    @property
    def remaining(self):
        """Вычесляет остаток до цели"""
        return max(Decimal(0), self.daily_goal - self.completed_m2)

    @property
    def average_m2_orders(self):
        """Вычесляет среднюю квадратуру заказов"""
        return 0 if self.completed_m2 == 0 or self.count_completed_orders == 0 else self.completed_m2 / self.count_completed_orders


class MonthlyStats(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    completed_m2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    count_completed_orders = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = ForeignKey(to=User, on_delete=CASCADE)

    class Meta:
        verbose_name = "Месячная статистика"
        verbose_name_plural = "Месячная статистика"

    def __str__(self):
        return f"{self.user} - Статистика за {self.month}.{self.year}"

    @property
    def progress_percentage(self):
        if self.monthly_goal == 0:
            return 0
        return min(100, int((self.completed_m2 / self.monthly_goal) * 100))

    @property
    def remaining(self):
        return max(Decimal(0), self.monthly_goal - self.completed_m2)

    @property
    def average_m2_orders(self):
        return 0 if self.completed_m2 == 0 or self.count_completed_orders == 0 else self.completed_m2 / self.count_completed_orders

    @property
    def average_m2_per_day(self):
        """Средняя квадратура за день в месяце"""
        if self.completed_m2 == 0:
            return Decimal(0)

        today = timezone.now().date()

        # Если это текущий месяц и год
        if self.year == today.year and self.month == today.month:
            # Используем количество прошедших дней в текущем месяце
            days_passed = today.day
        else:
            # Для прошлых месяцев используем общее количество дней в месяце
            _, days_passed = calendar.monthrange(self.year, self.month)

        # Избегаем деления на ноль
        if days_passed == 0:
            return Decimal(0)

        # Вычисляем среднюю квадратуру за день
        return self.completed_m2 / Decimal(days_passed)

    @property
    def is_current_month(self):
        """Проверяет, является ли месяц текущим"""
        today = timezone.now().date()
        return self.year == today.year and self.month == today.month

    @property
    def days_in_period(self):
        """Возвращает количество дней для расчета средней"""
        today = timezone.now().date()

        if self.year == today.year and self.month == today.month:
            # Текущий месяц - используем количество прошедших дней
            return today.day
        else:
            # Прошлый месяц - используем общее количество дней
            _, num_days = calendar.monthrange(self.year, self.month)
            return num_days

@property
def progress_percentage(self):
    if not self.daily_goal or self.daily_goal == 0:
        return 0
    try:
        return min(100, float((self.completed_m2 / self.daily_goal) * 100))
    except (TypeError, ValueError):
            return 0


