from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from shop.models import Order, OrderItem, Product, User


class OrderViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@gmail.com', password='password')
        self.order = Order.objects.create(
            user=self.user, order_no='No1234', created_at=timezone.now()
        )
        other_user = User.objects.create_user(email='user2@gmail.com', password='password')
        Order.objects.create(user=other_user, order_no='No5678', created_at=timezone.now())

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        Order.objects.all().delete()
        User.objects.all().delete()

    def test_get_order_list(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class SingleOrderViewTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            price=10,
            description='Test product description',
        )

        self.admin = User.objects.create_superuser(email='admin@gmail.com', password='password')
        self.user = User.objects.create_user(email='user@gmail.com', password='password')
        self.other_user = User.objects.create_user(email='user2@gmail.com', password='password')

        self.order = Order.objects.create(
            user=self.user, order_no='No1234', created_at=timezone.now()
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=2
        )

        self.other_user_order = Order.objects.create(
            user=self.other_user, order_no='No5678', created_at=timezone.now()
        )
        OrderItem.objects.create(order=self.other_user_order, product=self.product, quantity=3)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

    def test_get_order_detail(self):
        response = self.client.get(f'/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, 200)

    def test_get_other_user_order(self):
        response = self.client.get(f'/api/orders/{self.other_user_order.id}/')
        self.assertEqual(response.status_code, 403)

    def test_admin_get_order_detail(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f'/api/orders/{self.other_user_order.id}/')
        self.assertEqual(response.status_code, 200)

    def test_delete_order(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/orders/{self.order.id}/')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_non_admin_delete_order(self):
        response = self.client.delete(f'/api/orders/{self.order.id}/')

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Order.objects.filter(id=self.order.id).exists())


@override_settings(STORAGES={'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'}})
class OrderDeliveryStatusViewTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email='admin@gmail.com', password='password')
        self.user = User.objects.create_user(email='user@gmail.com', password='password')

        self.order = Order.objects.create(
            user=self.user, order_no='No1234', created_at=timezone.now()
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def tearDown(self):
        Order.objects.all().delete()
        User.objects.all().delete()

    def test_update_order_delivery_status(self):
        data = {'delivered': True}
        response = self.client.patch(f'/api/orders/{self.order.id}/status/', data, format='json')
        new_order = Order.objects.get(id=self.order.id)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(new_order.delivery_status)
