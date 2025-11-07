from django.urls import path
from .views import stats_dashboard, add_goal, GoalUpdateView

urlpatterns = [
    path('', stats_dashboard, name='stats_dashboard'),
    path('add_goal/', add_goal, name='add_goal'),
    path('goal_update/', GoalUpdateView.as_view(), name='goal_update')
]