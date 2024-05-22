from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from faker import Faker
from rest_framework.test import APIClient

from shop.models import Product, User


@override_settings(STORAGES={'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'}})
class ProductViewTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()

        self.user = User.objects.create_user(email='user@gmail.com', password='password')
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

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        Product.objects.all().delete()
        User.objects.all().delete()

    def test_get_product_list(self):
        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'name': self.faker.name(),
            'price': self.faker.random_int(min=1, max=100),
            'description': self.faker.text(),
            'image': SimpleUploadedFile(
                name='test.png',
                content=self.faker.image(image_format='png'),
                content_type='image/png',
            ),
        }
        response = self.client.post('/api/products/', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Product.objects.all()), 2)

    def test_create_product_with_non_admin(self):
        data = {
            'name': self.faker.name(),
            'price': self.faker.random_int(min=1, max=100),
            'description': self.faker.text(),
        }
        response = self.client.post('/api/products/', data)

        self.assertEqual(response.status_code, 403)


@override_settings(STORAGES={'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'}})
class SingleProductViewTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()

        self.user = User.objects.create_user(email='user@gmail.com', password='password')
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

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        Product.objects.all().delete()
        User.objects.all().delete()

    def test_get_product_detail(self):
        response = self.client.get(f'/api/products/{self.product.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(response.data['price'], self.product.price)
        self.assertEqual(response.data['description'], self.product.description)
        self.assertEqual(response.data['image'], f'http://testserver{self.product.image.url}')

    def test_update_product_name(self):
        self.client.force_authenticate(user=self.admin)
        data = {'name': 'New Name'}
        response = self.client.patch(f'/api/products/{self.product.id}/', data)
        new_product = Product.objects.get(id=self.product.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_product.name, data['name'])

    def test_update_product_price(self):
        self.client.force_authenticate(user=self.admin)
        data = {'price': 900}
        response = self.client.patch(f'/api/products/{self.product.id}/', data)
        new_product = Product.objects.get(id=self.product.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_product.price, data['price'])

    def test_update_product_description(self):
        self.client.force_authenticate(user=self.admin)
        data = {'description': 'New Description'}
        response = self.client.patch(f'/api/products/{self.product.id}/', data)
        new_product = Product.objects.get(id=self.product.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_product.description, data['description'])

    def test_update_product_image(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'image': SimpleUploadedFile(
                name='new.png',
                content=self.faker.image(image_format='png'),
                content_type='image/png',
            ),
        }
        response = self.client.patch(f'/api/products/{self.product.id}/', data)
        new_product = Product.objects.get(id=self.product.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_product.image.name, f'products/{data["image"].name}')

    def test_update_product_with_non_admin(self):
        data = {'name': 'New Name'}
        response = self.client.patch(f'/api/products/{self.product.id}/', data)

        self.assertEqual(response.status_code, 403)

    def test_delete_product(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/products/{self.product.id}/')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_delete_product_with_non_admin(self):
        response = self.client.delete(f'/api/products/{self.product.id}/')

        self.assertEqual(response.status_code, 403)
