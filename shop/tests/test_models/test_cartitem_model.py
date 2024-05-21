from django.test import TestCase

from shop.models import CartItem, Product, User


class CartItemModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@gmail.com', password='password')
        self.product = Product.objects.create(
            name='Test Product',
            price=100,
            description='This is a test product.',
        )
        self.cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)

    def tearDown(self):
        User.objects.all().delete()
        Product.objects.all().delete()
        CartItem.objects.all().delete()

    def test_total_property(self):
        # total = price * quantity
        self.assertEqual(self.cart_item.total, 200)

    def test_unique_together_attribute(self):
        unique_together = CartItem._meta.unique_together

        # make sure cart-item can't be created with the same user and product
        self.assertTrue(unique_together.__contains__(('user', 'product')))
