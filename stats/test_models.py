from django.test import TestCase
from django.contrib.auth import get_user_model

from stats.models import GoalSettings, DailyStats, MonthlyStats

class DailyStatsModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.daily_stat = DailyStats.objects.create(
            user=self.user,
            completed_m2=200.00,
            daily_goal=300.00,
            count_completed_orders=1.00,
        )

    def test_progress_percentage(self):
        """Проверка правильности вычисления процентов до цели"""
        self.assertEqual(self.daily_stat.progress_percentage, 66)

    def test_remaining(self):
        """Проверка остатка до цели"""
        self.assertEqual(self.daily_stat.remaining, 100.00)

    def test_average_m2_orders(self):
        """Проверка средней квадратуры заказов"""
        self.assertEqual(self.daily_stat.average_m2_orders, 200.00)

class MonthlyStatsModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.monthly_stat = MonthlyStats.objects.create(
            user=self.user,
            completed_m2=300.00,
            monthly_goal=9000.00,
            count_completed_orders=5.00,
            year=2025,
            month=11
        )

    def test_progress_percentage(self):
        """Проверка правильности вычисления процентов до цели"""
        self.assertEqual(self.monthly_stat.progress_percentage, 3)

    def test_remaining(self):
        """Проверка остатка до цели"""
        self.assertEqual(self.monthly_stat.remaining, 8700.00)

    def test_average_m2_orders(self):
        """Проверка средней квадратуры заказов"""
        self.assertEqual(self.monthly_stat.average_m2_orders, 60.00)

