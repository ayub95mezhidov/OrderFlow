from django.db import models
from django.db.models import CASCADE, ForeignKey

from users.models import User


class PriceSettings(models.Model):
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

    fabric_size = models.CharField(
        max_length=20,
        choices=FABRIC_SIZE_CHOICES,
        verbose_name="Размер ткани",
        unique=False
    )
    ceiling_type = models.CharField(
        max_length=20,
        choices=CEILING_TYPE_CHOICES,
        verbose_name="Тип потолка",
    )
    price_m2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за м²",
    )

    user = ForeignKey(to=User, on_delete=CASCADE)

    class Meta:
        unique_together = ('fabric_size', 'ceiling_type', 'user')
        verbose_name = "Настройка цены"
        verbose_name_plural = "Настройки цен"

    def __str__(self):
        return f"{self.user} {self.get_fabric_size_display()} + {self.get_ceiling_type_display()} - {self.price_m2} ₽/м²"


class PriceAccessories(models.Model):
    accessories = models.CharField(max_length=256, verbose_name='Комплектующий')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    user = ForeignKey(to=User, on_delete=CASCADE, related_name='price_accessories')  # добавляем уникальное related_name

    class Meta:
        verbose_name = "Настройка цены комплектующих"
        verbose_name_plural = "Настройки цен комплектующих"

    def __str__(self):
        return f"{self.accessories} - {self.price} ₽"