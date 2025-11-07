from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from orders.models import Order
from .models import DailyStats, MonthlyStats

@receiver(pre_save, sender=Order)
def store_old_status(sender, instance, **kwargs):
    """Перед сохранением сохраняем старый статус"""
    if instance.pk:
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Order)
def update_stats_on_order_save(sender, instance, **kwargs):
    # Проверяем, стал ли заказ "completed" только сейчас
    if instance.status == 'completed' and instance._old_status != 'completed':
        today = timezone.now().date()
        if instance.completed_at:
            today = instance.completed_at.date()

        month = today.month
        year = today.year

        daily_stat, _ = DailyStats.objects.get_or_create(
            user=instance.user,
            date=today,
        )

        monthly_stat, _ = MonthlyStats.objects.get_or_create(
            user=instance.user,
            year=year,
            month=month,
        )

        # Пересчитываем квадратуру по completed_at
        daily_stat.completed_m2 = sum(
            order.square for order in Order.objects.filter(
                user=instance.user,
                completed_at__date=today,
                status='completed'
            )
        )
        daily_stat.save()

        monthly_stat.completed_m2 = sum(
            order.square for order in Order.objects.filter(
                user=instance.user,
                completed_at__year=year,
                completed_at__month=month,
                status='completed'
            )
        )
        monthly_stat.save()

        # Пересчитываем кол-во завершенных заказов по completed_at
        daily_stat.count_completed_orders = Order.objects.filter(
            user=instance.user,
            completed_at__date=today,
            status='completed'
        ).count()
        daily_stat.save()

        monthly_stat.count_completed_orders = Order.objects.filter(
            user=instance.user,
            completed_at__year=year,
            completed_at__month=month,
            status='completed'
        ).count()
        monthly_stat.save()