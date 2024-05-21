from django.test import TestCase
from django.utils import timezone

from shop.models import Order, OrderItem, Product, User


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@gmail.com', password='password')
        self.product = Product.objects.create(
            name='Test Product',
            price=100,
            description='This is a test product.',
        )
        self.order = Order.objects.create(
            user=self.user, order_no='No1234', created_at=timezone.now()
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=5,
        )

    def tearDown(self):
        self.order_item.delete()
        self.order.delete()
        self.product.delete()
        self.user.delete()

    def test_total_property(self):
        # total = price * quantity
        self.assertEqual(self.order_item.total, 500)

    def test_unique_together_attribute(self):
        unique_together = OrderItem._meta.unique_together

        # make sure order-item can't be created with the same order and product
        self.assertTrue(unique_together.__contains__(('order', 'product')))
