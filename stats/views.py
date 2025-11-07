from django.shortcuts import render, redirect
from django.utils import timezone
from .models import DailyStats, MonthlyStats, GoalSettings
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import GoalForm
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.db.models import Q

@login_required(login_url='/users/login/')
def stats_dashboard(request):
    today = timezone.now().date()
    month = today.month
    year = today.year

    # Получаем параметры для навигации по месяцам
    selected_year = request.GET.get('year', year)
    selected_month = request.GET.get('month', month)

    try:
        selected_year = int(selected_year)
        selected_month = int(selected_month)
    except (ValueError, TypeError):
        selected_year = year
        selected_month = month

    goals = GoalSettings.objects.filter(user=request.user).first()
    if goals is not None:
        try:

            # Получаем или создаем статистику с дефолтными значениями
            daily_stats, _ = DailyStats.objects.get_or_create(
                user=request.user,
                date=today,
                defaults={'daily_goal': goals.daily_goal, 'completed_m2': Decimal('0')}
            )

            monthly_stats, _ = MonthlyStats.objects.get_or_create(
                user=request.user,
                year=year,
                month=month,
                defaults={'monthly_goal': goals.monthly_goal, 'completed_m2': Decimal('0')}
            )




        except GoalSettings.DoesNotExist:
            daily_stats = 'Нет цели дня'
            monthly_stats = 'Нет цели месяца'
    else:
        daily_stats = 'Нет цели дня'
        monthly_stats = 'Нет цели месяца'

    daily_stats_all = DailyStats.objects.filter(user=request.user).order_by('-date')
    monthly_stats_all = MonthlyStats.objects.filter(user=request.user).order_by('-year', '-month')

    # Группируем дневную статистику по месяцам
    daily_stats_by_month = defaultdict(list)
    for stat in daily_stats_all:
        month_key = f"{stat.date.year}-{stat.date.month:02d}"
        daily_stats_by_month[month_key].append(stat)

    # Сортируем месяцы по убыванию
    sorted_month_keys = sorted(daily_stats_by_month.keys(), reverse=True)

    # Получаем статистику для выбранного месяца
    selected_month_key = f"{selected_year}-{selected_month:02d}"
    selected_month_stats = daily_stats_by_month.get(selected_month_key, [])

    # Вычисляем итоги для выбранного месяца
    if selected_month_stats:
        total_completed = sum(float(stat.completed_m2) for stat in selected_month_stats)
        total_goal = sum(float(stat.daily_goal) for stat in selected_month_stats)
        total_orders = sum(float(stat.count_completed_orders) for stat in selected_month_stats)

        progress_percentage = (total_completed / total_goal * 100) if total_goal > 0 else 0
        avg_per_order = total_completed / total_orders if total_orders > 0 else 0

        selected_month_data = {
            'stats_list': selected_month_stats,
            'total_completed': total_completed,
            'total_goal': total_goal,
            'total_orders': total_orders,
            'progress_percentage': progress_percentage,
            'avg_per_order': avg_per_order,
            'month_name': selected_month_stats[0].date.strftime("%B %Y"),
            'days_count': len(selected_month_stats)
        }


    # Вычисляем навигацию по месяцам
    prev_month, prev_year = get_previous_month(selected_year, selected_month)
    next_month, next_year = get_next_month(selected_year, selected_month)

    # Проверяем, есть ли данные для соседних месяцев
    prev_month_key = f"{prev_year}-{prev_month:02d}"
    next_month_key = f"{next_year}-{next_month:02d}"

    has_prev_month = prev_month_key in daily_stats_by_month
    has_next_month = next_month_key in daily_stats_by_month

    context = {
        'daily_stats': daily_stats,
        'monthly_stats': monthly_stats,
        'today': today,
        'daily_stats_all': daily_stats_all,
        'monthly_stats_all': monthly_stats_all,
        'selected_month_data': selected_month_data,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'has_prev_month': has_prev_month,
        'has_next_month': has_next_month,
        'available_months': sorted_month_keys,  # Все доступные месяцы для информации
    }
    return render(request, 'stats/dashboard.html', context)

def get_previous_month(year, month):
    """Возвращает предыдущий месяц"""
    if month == 1:
        return 12, year - 1
    else:
        return month - 1, year

def get_next_month(year, month):
    """Возвращает следующий месяц"""
    if month == 12:
        return 1, year + 1
    else:
        return month + 1, year

@login_required(login_url='/users/login/')
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('stats_dashboard')
    else:
        form = GoalForm()
    context = {
        'form': form,
    }
    return render(request, 'stats/add_goal.html', context)

class GoalUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login/'
    model = GoalSettings
    form_class = GoalForm
    template_name = 'stats/goal_update.html'
    success_url = reverse_lazy('stats_dashboard')

    def get_object(self, queryset=None):
        # Получаем или создаем настройки для текущего пользователя
        obj, created = GoalSettings.objects.get_or_create(user=self.request.user)
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        today = timezone.now().date()

        # Обновляем дневную статистику для сегодня и будущих дней
        DailyStats.objects.filter(
            user=self.request.user,
            date__date__gte=today
        ).update(daily_goal=self.object.daily_goal)

        # Обновляем месячную статистику для текущего и следующих месяцев
        current_year = today.year
        current_month = today.month
        MonthlyStats.objects.filter(user=self.request.user).filter(
            Q(year=current_year, month__gte=current_month) |
            Q(year__gt=current_year)
        ).update(monthly_goal=self.object.monthly_goal)

        return response