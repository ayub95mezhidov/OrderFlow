from django.test import TestCase
from django.contrib.auth import get_user_model

from stats.models import GoalSettings, DailyStats, MonthlyStats

class DailyStatsViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
