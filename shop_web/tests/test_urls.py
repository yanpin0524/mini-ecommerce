from django.test import Client, TestCase
from faker import Faker

from shop.models import Product


class TestShopUrls(TestCase):
    def setUp(self):
        self.client = Client()
        self.faker = Faker()

        self.product = Product.objects.create(
            name=self.faker.text(70),
            price=self.faker.pyfloat(3, 2, 1, True),
            description=self.faker.text(200),
        )

    def test_shop_page(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page(self):
        response = self.client.get(f'/products/{self.product.id}/')
        self.assertEqual(response.status_code, 200)
