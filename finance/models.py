from django.db import models
from django.db.models import CASCADE, ForeignKey

from users.models import User

class Wallet(models.Model):
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(to=User, on_delete=CASCADE,)

    def __str__(self):
        return f'{self.user} - {self.cash}'

class Debt(models.Model):
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(to=User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} - {self.debt}'

class CategoryIncome(models.Model):
    COLOR_CHOICES = [
        ('Красный', 'Red'),
        ('Синий', 'Blue'),
        ('Зеленый', 'Green'),
        ('Желтый', 'Yellow'),
        ('Оранжевый', 'Orange'),
        ('Фиолетовый', 'Purple'),
        ('Розовый', 'Pink'),
        ('Коричневый', 'Brown'),
        ('Черный', 'Black'),
        ('Белый', 'White'),
        ('Серый', 'Gray' ),
    ]

    title = models.CharField(max_length=128)
    color = models.CharField(max_length=128, choices=COLOR_CHOICES)
    user = models.ForeignKey(to=User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} - {self.title}'

class CategoryExpenses(models.Model):
    COLOR_CHOICES = [
        ('Красный', 'Red'),
        ('Синий', 'Blue'),
        ('Зеленый', 'Green'),
        ('Желтый', 'Yellow'),
        ('Оранжевый', 'Orange'),
        ('Фиолетовый', 'Purple'),
        ('Розовый', 'Pink'),
        ('Коричневый', 'Brown'),
        ('Черный', 'Black'),
        ('Белый', 'White'),
        ('Серый', 'Gray' ),
    ]

    title = models.CharField(max_length=128)
    color = models.CharField(max_length=128, choices=COLOR_CHOICES)
    user = models.ForeignKey(to=User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} - {self.title}'

class Income(models.Model):
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    title = ForeignKey(to=CategoryIncome, on_delete=CASCADE)
    date = models.DateTimeField(blank=False)
    user = models.ForeignKey(to=User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} - {self.title} {self.total_sum}'


class Expenses(models.Model):
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    title = ForeignKey(to=CategoryExpenses, on_delete=CASCADE)
    date = models.DateTimeField(blank=False)
    user = models.ForeignKey(to=User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} - {self.title} {self.total_sum}'
