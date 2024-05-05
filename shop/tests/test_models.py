import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from shop.models import CartItem, Order, OrderItem, Product, User


class UserModelTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def test_create_user(self):
        user = User.objects.create_user(email='user@gmail.com', password='password')

        self.assertEqual(user.email, 'user@gmail.com')
        self.assertTrue(user.check_password('password'))

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='superuser@gmail.com', password='password')

        self.assertEqual(superuser.email, 'superuser@gmail.com')
        self.assertTrue(superuser.check_password('password'))

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='password')

    def test_create_user_no_password(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='user@gmail.com', password=None)

    def test_email_field(self):
        email_field = User._meta.get_field('email')
        self.assertEqual(email_field.max_length, 255)
        self.assertTrue(email_field.unique)


class ProductModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg',
        )

        cls.product = Product.objects.create(
            name='product1',
            price=100,
            description="This is product1's description.",
            image=cls.test_image,
        )

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        os.remove(f'images/products/{cls.test_image.name}')

    def test_create_product(self):
        self.assertEqual(self.product.name, 'product1')
        self.assertEqual(self.product.price, 100)
        self.assertEqual(self.product.description, "This is product1's description.")
        self.assertEqual(self.product.image.name, f'products/{self.test_image.name}')

    def test_name_field(self):
        name_field = self.product._meta.get_field('name')
        self.assertEqual(name_field.max_length, 70)

    def test_price_field(self):
        price_field = self.product._meta.get_field('price')
        self.assertEqual(price_field.max_digits, 10)
        self.assertEqual(price_field.decimal_places, 2)


class CartItemModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_image = SimpleUploadedFile(
            name='test_image2.jpg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg',
        )

        cls.user = User.objects.create_user(email='user@gmail.com', password='password')
        cls.product = Product.objects.create(
            name='product1',
            price=100,
            description="This is product1's description.",
            image=cls.test_image,
        )
        cls.cart_item = CartItem.objects.create(user=cls.user, product=cls.product, quantity=2)

    @classmethod
    def tearDownClass(cls):
        CartItem.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

        os.remove(f'images/products/{cls.test_image.name}')

    def test_create_cart_item(self):
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)


class OrderModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email='user@gmail.com', password='password')
        cls.order = Order.objects.create(user=user)

    @classmethod
    def tearDownClass(cls):
        Order.objects.all().delete()
        User.objects.all().delete()

    def test_create_order(self):
        self.assertEqual(self.order.user.email, 'user@gmail.com')
        self.assertFalse(self.order.delivery_status)


class OrderItemModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_image = SimpleUploadedFile(
            name='test_image3.jpg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg',
        )

        cls.user = User.objects.create_user(email='user@gmail.com', password='password')
        cls.product = Product.objects.create(
            name='product1',
            price=100,
            description="This is product1's description.",
            image=cls.test_image,
        )
        cls.order = Order.objects.create(user=cls.user)
        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            product=cls.product,
            price=cls.product.price,
            quantity=2,
        )

    @classmethod
    def tearDownClass(cls):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

        os.remove(f'images/products/{cls.test_image.name}')

    def test_create_order_item(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.price, self.product.price)
        self.assertEqual(self.order_item.quantity, 2)

    def test_price_field(self):
        price_field = self.order_item._meta.get_field('price')
        self.assertEqual(price_field.max_digits, 10)
        self.assertEqual(price_field.decimal_places, 2)
