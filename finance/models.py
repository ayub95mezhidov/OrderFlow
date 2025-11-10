from django.db import models
from django.db.models import CASCADE

from users.models import User

class Wallet(models.Model):
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(to=User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} - {self.cash}'

class Debt(models.Model):
    debt = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(to=User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} - {self.debt}'
