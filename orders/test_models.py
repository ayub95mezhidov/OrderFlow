from django.test import TestCase
from decimal import Decimal

from .models import Order, Customer, Accessories
from settings.models import PriceSettings, PriceAccessories
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='password')
        customer = Customer.objects.create(full_name='Ayub Mezhidov', phone_number='123456789', user=user)
        self.order = Order.objects.create(
            customer=customer,
            user=user,
            width=5.00,
            length=10.00,
            fabric_size='short',
            ceiling_type='white mat',
        )

    def test_square_property(self):
        """Проверка правильности вычисления площади"""
        self.assertEqual(self.order.square, 50.00)

    def test_perimeter_property(self):
        """Проверка правильности вычисления периметра"""
        self.assertEqual(self.order.perimeter, 30.00)

    def test_total_sum_property(self):
        """Проверка правильности вычисления суммы заказа"""
        price_setting = PriceSettings.objects.create(
            user=self.order.user,
            fabric_size='short',
            ceiling_type='white mat',
            price_m2=100.00)
        self.assertEqual(self.order.total_sum, Decimal('5000.00'))

class AccessoriesModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='password')
        customer = Customer.objects.create(full_name='John Doe', phone_number='123456789', user=user)
        price_accessory = PriceAccessories.objects.create(user=user, accessories='Accessory 1', price=200.00)
        self.accessory = Accessories.objects.create(
            customer=customer,
            user=user,
            accessories=price_accessory,
            quantity=2
        )

    def test_accessories_total(self):
        """Проверка правильности вычисления стоимости комплектующих"""
        self.assertEqual(self.accessory.accessories_total, 400.00)