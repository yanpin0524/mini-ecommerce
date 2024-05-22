from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from faker import Faker
from rest_framework.test import APIClient

from shop.models import CartItem, Product, User


@override_settings(STORAGES={'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'}})
class CartItemViewTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()

        self.user = User.objects.create_user(email='user@gmail.com', password='password')
        self.other_user = User.objects.create_user(email='user2@gmail.com', password='password')
        self.product = Product.objects.create(
            name=self.faker.name(),
            price=self.faker.random_int(min=1, max=100),
            description=self.faker.text(),
            image=SimpleUploadedFile(
                name='test.png',
                content=self.faker.image(image_format='png'),
                content_type='image/png',
            ),
        )
        self.cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        # another user's cart item, this one should not be available
        CartItem.objects.create(user=self.other_user, product=self.product, quantity=2)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        CartItem.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

    def test_get_cart_item_list(self):
        response = self.client.get('/api/cart/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_cart_item(self):
        product2 = Product.objects.create(
            name=self.faker.name(),
            price=self.faker.random_int(min=1, max=100),
            description=self.faker.text(),
        )

        data = {'product_id': product2.id, 'quantity': 3}
        response = self.client.post('/api/cart/', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(CartItem.objects.filter(user=self.user)), 2)

    def test_clear_cart(self):
        response = self.client.delete('/api/cart/')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(CartItem.objects.filter(user=self.user)), 0)
        self.assertEqual(len(CartItem.objects.all()), 1)


@override_settings(STORAGES={'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'}})
class SingleCartItemViewTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()

        self.user = User.objects.create_user(email='user@gmail.com', password='password')
        self.other_user = User.objects.create_user(email='user2@gmail.com', password='password')
        self.admin = User.objects.create_superuser(email='admin@gmail.com', password='password')
        self.product = Product.objects.create(
            name=self.faker.name(),
            price=self.faker.random_int(min=1, max=100),
            description=self.faker.text(),
            image=SimpleUploadedFile(
                name='test.png',
                content=self.faker.image(image_format='png'),
                content_type='image/png',
            ),
        )
        self.cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        self.other_user_cart_item = CartItem.objects.create(
            user=self.other_user, product=self.product, quantity=2
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        CartItem.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

    def test_delete_cart_item(self):
        response = self.client.delete(f'/api/cart/{self.cart_item.id}/')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(CartItem.objects.all()), 1)

    def test_delete_other_user_cart_item(self):
        response = self.client.delete(f'/api/cart/{self.other_user_cart_item.id}/')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(CartItem.objects.all()), 2)

    def test_delete_cart_item_with_admin(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(f'/api/cart/{self.cart_item.id}/')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(CartItem.objects.all()), 1)


class CartItemQuantityViewTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()

        self.admin = User.objects.create_superuser(email='admin@gmail.com', password='password')
        self.user = User.objects.create_user(email='user@gmail.com', password='password')
        self.other_user = User.objects.create_user(email='user2@gmail.com', password='password')
        self.product = Product.objects.create(
            name=self.faker.name(),
            price=self.faker.random_int(min=1, max=100),
            description=self.faker.text(),
        )
        self.cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)

        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def tearDown(self):
        CartItem.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

    def test_update_cart_item_quantity(self):
        data = {'quantity': 3}
        response = self.client.patch(f'/api/cart/{self.cart_item.id}/quantity/', data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.get(id=self.cart_item.id).quantity, 3)

    def test_non_owner_update_cart_item_quantity(self):
        self.client.force_authenticate(user=self.other_user)
        data = {'quantity': 3}
        response = self.client.patch(f'/api/cart/{self.cart_item.id}/quantity/', data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(CartItem.objects.get(id=self.cart_item.id).quantity, 2)

    def test_admin_update_cart_item_quantity(self):
        data = {'quantity': 3}
        response = self.client.patch(f'/api/cart/{self.cart_item.id}/quantity/', data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.get(id=self.cart_item.id).quantity, 3)
