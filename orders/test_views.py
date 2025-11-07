from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from orders.models import Customer, Order


class OrderViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.customer = Customer.objects.create(full_name='Daud Mezhidov', phone_number='123456789', user=self.user)

    def test_add_order_view(self):
        """Тестирование создание заказа"""
        url = reverse('add_order_for_customer', kwargs={'customer_id': self.customer.id})
        response = self.client.post(url, {
            'customer': self.customer.id,
            'width': 5.00,
            'length': 10.00,
            'fabric_size': 'wide',
            'ceiling_type': 'white mat',
            'payment_status': 'not paid',
            'status': 'new'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу с заказами
        self.assertEqual(Order.objects.count(), 1)  # Проверяем, что заказ был добавлен

class CustomerListViewTest(TestCase):
    def setUp(self):
        """Создание тестового пользователя и клиентов"""
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.customer1 = Customer.objects.create(full_name='John Doe', phone_number='123456789', user=self.user)
        self.customer2 = Customer.objects.create(full_name='Jane Doe', phone_number='987654321', user=self.user)

    def test_customer_list_view(self):
        """Тестирование отображения списка клиентов"""
        url = reverse('customers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer1.full_name)
        self.assertContains(response, self.customer2.full_name)

    def test_customer_search(self):
        """Тестирование поиска клиентов по имени"""
        url = reverse('customers') + '?search_query=John'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer1.full_name)
        self.assertNotContains(response, self.customer2.full_name)

class OrderPaymentStatusUpdateTest(TestCase):
    def setUp(self):
        """Создание тестового пользователя и заказа"""
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.customer = Customer.objects.create(full_name='John', phone_number='123456789', user=self.user)
        self.order = Order.objects.create(
            customer=self.customer,
            user=self.user,
            width=5.00,
            length=10.00,
            fabric_size='wide',
            ceiling_type='white mat',
            payment_status='not paid',
            status='new'
        )

    def test_update_payment_status(self):
        """Тестирование изменения статуса оплаты заказа"""
        url = reverse('update_payment_status', kwargs={'order_id': self.order.id})
        response = self.client.post(url, {'payment_status': 'paid'})
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, 'paid')
        self.assertEqual(response.status_code, 200)