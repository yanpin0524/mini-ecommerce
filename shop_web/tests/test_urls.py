from django.test import Client, TestCase
from django.utils import timezone
from faker import Faker

from shop.models import CartItem, Order, OrderItem, Product, User


class SignInUrlsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='user@gmail.com', password='password')

    def test_sign_in_page(self):
        response = self.client.get('/sign-in/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_in.html')

    def test_sign_in_form(self):
        data = {'username': 'user@gmail.com', 'password': 'password'}
        response = self.client.post('/sign-in/', data)

        self.assertEqual(response.status_code, 302)


class SignUpUrlsTestCase(TestCase):
    def test_sign_up_page(self):
        response = self.client.get('/sign-up/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')

    def test_sign_up_form(self):
        data = {'email': 'user@gmail.com', 'password': 'password', 'confirm_password': 'password'}
        response = self.client.post('/sign-up/', data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)


class ProductUrlsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.faker = Faker()

        self.product = Product.objects.create(
            name=self.faker.text(70),
            price=self.faker.random_int(min=1, max=100),
            description=self.faker.text(200),
        )

    def test_product_list_page(self):
        response = self.client.get('/products/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')

    def test_product_detail_page(self):
        response = self.client.get(f'/products/{self.product.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')


class CartUrlsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.faker = Faker()

        self.user = User.objects.create_user(email='user@gmail.com', password='password')
        self.client.force_login(self.user)

        self.product = Product.objects.create(
            name=self.faker.text(70),
            price=self.faker.random_int(min=1, max=100),
            description=self.faker.text(200),
        )

    def tearDown(self):
        self.client.logout()
        Product.objects.all().delete()
        User.objects.all().delete()

    def test_cart_list_page(self):
        response = self.client.get('/cart/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_list.html')

    def test_cart_add_form(self):
        data = {'quantity': 2}
        response = self.client.post(
            f'/cart/{self.product.id}/add/', data, HTTP_REFERER=f'/products/{self.product.id}/'
        )

        self.assertEqual(response.status_code, 302)

    def test_cart_remove_form(self):
        CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        response = self.client.post(f'/cart/{self.product.id}/remove/')

        self.assertEqual(response.status_code, 302)


class OrderUrlsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.faker = Faker()

        self.user = User.objects.create_user(email='user@gmail.com', password='password')
        self.client.force_login(self.user)

        self.product = Product.objects.create(
            name=self.faker.text(70),
            price=self.faker.random_int(min=1, max=100),
            description=self.faker.text(200),
        )

        self.order = Order.objects.create(
            user=self.user, order_no='No1234', created_at=timezone.now()
        )

        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=2
        )

    def tearDown(self):
        self.client.logout()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

    def test_order_list_page(self):
        response = self.client.get('/orders/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_list.html')

    def test_order_detail_page(self):
        response = self.client.get(f'/orders/{self.order.order_no}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_detail.html')
        self.assertEqual(len(response.context.get('order_items')), 1)
