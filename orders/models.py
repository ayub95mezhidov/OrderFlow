
from django.db import models
from django.db.models import ForeignKey, CASCADE
from decimal import Decimal

from settings.models import PriceAccessories
from users.models import User

class Customer(models.Model):
    full_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20)
    user = ForeignKey(to=User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.full_name}'

class Order(models.Model):
    FABRIC_SIZE_CHOICES = [
        ('short', '1.5м - 3.6м'),
        ('wide', '4.0м - 5.0м'),
        ('the widest', '5.8м'),
    ]
    CEILING_TYPE_CHOICES = [
        ('white mat', 'Белый мат'),
        ('colored mat', 'Цветной мат'),
        ('white gloss', 'Белый лак'),
        ('colored gloss', 'Цветной лак'),
        ('white sateen', 'Белый сатин'),
        ('colored sateen', 'Цветной сатин'),
        ('venice', 'Венеция'),
        ('sky', 'Небо'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершен'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('not paid', 'Не оплачено'),
        ('paid', 'Оплачено')
    ]

    customer = ForeignKey(to=Customer, on_delete=CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    fabric_size = models.CharField(max_length=10,choices=FABRIC_SIZE_CHOICES)
    ceiling_type = models.CharField(max_length=14, choices=CEILING_TYPE_CHOICES)
    photo = models.ImageField(upload_to='order_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICES, default='not paid')
    user = ForeignKey(to=User, on_delete=CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def perimeter(self):
        """Периметр заказа"""
        return (self.width + self.length) * 2

    @property
    def square(self):
        """"Квадратура заказа"""
        return self.width * self.length

    def price(self):
        """Цена за кв. м. заказа"""
        from settings.models import PriceSettings
        try:
            price_setting = PriceSettings.objects.get(
                user=self.user,
                fabric_size=self.fabric_size,
                ceiling_type=self.ceiling_type,
            )
            return price_setting.price_m2
        except PriceSettings.DoesNotExist:
            return Decimal(0)

    @property
    def total_sum(self):
        """Сумма заказа"""
        from settings.models import PriceSettings
        try:
            price_setting = PriceSettings.objects.get(
                user=self.user,
                fabric_size=self.fabric_size,
                ceiling_type=self.ceiling_type,
            )
            return Decimal(self.square) * price_setting.price_m2
        except PriceSettings.DoesNotExist:
            return Decimal(0)

    @property
    def balance(self):
        return self.total_sum

    def __str__(self):
        return f'Заказ #{self.id} - {self.customer.full_name}'

class Accessories(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('not paid', 'Не оплачено'),
        ('paid', 'Оплачено')
    ]

    user = ForeignKey(to=User, on_delete=CASCADE)
    customer = ForeignKey(to=Customer, on_delete=CASCADE)
    accessories = models.ForeignKey(
        PriceAccessories,
        on_delete=models.SET_NULL,  # или CASCADE в зависимости от логики
        null=True,
        blank=True,
        verbose_name='Комплектующий',
        limit_choices_to={'user': models.F('user')},
        related_name = 'accessories_orders'
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=1, default=0, verbose_name='Количество')
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICES, default='not paid')

    @property
    def accessories_total(self):
        """Сумма стоимости всех комплектующих"""
        if self.accessories and self.accessories.price:
            return Decimal(self.accessories.price * self.quantity)
        return Decimal(0)

    def __str__(self):
        return f'{self.accessories} {self.accessories_total}'

