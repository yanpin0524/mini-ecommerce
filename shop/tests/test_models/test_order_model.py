from django.test import TestCase

from shop.models import Order


class OrderModelTestCase(TestCase):
    def test_order_no_field(self):
        order_no_field = Order._meta.get_field('order_no')
        self.assertEqual(order_no_field.max_length, 20)
        self.assertTrue(order_no_field.unique)

    def test_delivery_status_field(self):
        delivery_status_field = Order._meta.get_field('delivery_status')
        self.assertEqual(delivery_status_field.default, False)
