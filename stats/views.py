from django.shortcuts import render, redirect
from django.utils import timezone
from .models import DailyStats, MonthlyStats, GoalSettings
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import GoalForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import calendar
from django.db.models import Sum


@login_required(login_url='/users/login/')
def stats_dashboard(request):
    today = timezone.now().date()

    # Получаем параметры для навигации
    selected_year = request.GET.get('year', today.year)
    selected_month = request.GET.get('month', today.month)

    try:
        selected_year = int(selected_year)
        selected_month = int(selected_month)
    except (ValueError, TypeError):
        selected_year = today.year
        selected_month = today.month

    # Получаем цели пользователя
    goals = GoalSettings.objects.filter(user=request.user).first()

    # Инициализируем переменные
    daily_stats = None
    monthly_stats = None

    if goals:
        # Получаем или создаем статистику за сегодня
        daily_stats, _ = DailyStats.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={
                'daily_goal': goals.daily_goal,
                'completed_m2': Decimal('0'),
                'count_completed_orders': 0
            }
        )

        # Получаем или создаем статистику за текущий месяц
        monthly_stats, _ = MonthlyStats.objects.get_or_create(
            user=request.user,
            year=today.year,
            month=today.month,
            defaults={
                'monthly_goal': goals.monthly_goal,
                'completed_m2': Decimal('0'),
                'count_completed_orders': 0
            }
        )

    # Определяем первый и последний день выбранного месяца
    _, last_day = calendar.monthrange(selected_year, selected_month)
    start_date = timezone.datetime(selected_year, selected_month, 1).date()
    end_date = timezone.datetime(selected_year, selected_month, last_day).date()

    # Получаем данные ТОЛЬКО для выбранного месяца
    selected_month_stats = DailyStats.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('-date')

    # Вычисляем агрегированные данные для выбранного месяца
    selected_month_data = None
    if selected_month_stats.exists():
        aggregated = selected_month_stats.aggregate(
            total_completed=Sum('completed_m2'),
            total_goal=Sum('daily_goal'),
            total_orders=Sum('count_completed_orders')
        )

        total_completed = float(aggregated['total_completed'] or 0)
        total_goal = float(aggregated['total_goal'] or 0)
        total_orders = float(aggregated['total_orders'] or 0)

        progress_percentage = (total_completed / total_goal * 100) if total_goal > 0 else 0
        avg_per_order = total_completed / total_orders if total_orders > 0 else 0

        # Правильное название месяца на русском
        month_names = {
            1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
            5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
            9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
        }
        month_name = f"{month_names[selected_month]} {selected_year}"

        selected_month_data = {
            'stats_list': selected_month_stats,
            'total_completed': total_completed,
            'total_goal': total_goal,
            'total_orders': total_orders,
            'progress_percentage': progress_percentage,
            'avg_per_order': avg_per_order,
            'month_name': month_name,
            'days_count': selected_month_stats.count(),
            'start_date': start_date,
            'end_date': end_date
        }

    # Навигация по месяцам с проверкой существования данных
    prev_month, prev_year = get_previous_month(selected_year, selected_month)
    next_month, next_year = get_next_month(selected_year, selected_month)

    # проверка существования данных для соседних месяцев
    prev_has_data = DailyStats.objects.filter(
        user=request.user,
        date__year=prev_year,
        date__month=prev_month
    ).exists()

    next_has_data = DailyStats.objects.filter(
        user=request.user,
        date__year=next_year,
        date__month=next_month
    ).exists()

    context = {
        'daily_stats': daily_stats,
        'monthly_stats': monthly_stats,
        'today': today,
        'selected_month_data': selected_month_data,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'has_prev_month': prev_has_data,
        'has_next_month': next_has_data,
        'has_goals': goals is not None,
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