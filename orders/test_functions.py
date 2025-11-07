from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from orders.models import Customer, Order, Accessories
from orders.views import calculate_customer_debt
from settings.models import PriceAccessories, PriceSettings

class CalculateCustomerDebtTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', password='password')
        #self.client.login(username='testuser', password='password')
        self.customer = Customer.objects.create(full_name='John', phone_number='123456789', user=self.user)
        self.order = Order.objects.create(
            customer=self.customer,
            user=self.user,
            width=5.00,
            length=10.00,
            fabric_size='short',
            ceiling_type='white mat',
        )

        price_accessory = PriceAccessories.objects.create(user=self.user, accessories='Accessory 1', price=200.00)
        self.accessory = Accessories.objects.create(
            user=self.user,
            customer=self.customer,
            accessories=price_accessory,
            quantity=2
        )

    def test_customer_debt(self):
        """"Тестирование функции calculate_customer_debt"""
        price_ceil = PriceSettings.objects.create(fabric_size='short', ceiling_type='white mat', price_m2=100.00,
                                                  user=self.user)
        self.assertEqual(calculate_customer_debt(self.customer), Decimal('5400'))