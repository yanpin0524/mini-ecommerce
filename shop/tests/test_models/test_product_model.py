from django.test import TestCase

from shop.models import Product


class ProductModelTestCase(TestCase):
    def test_name_field(self):
        name_field = Product._meta.get_field('name')
        self.assertEqual(name_field.max_length, 70)

    def test_image_field(self):
        image_field = Product._meta.get_field('image')
        self.assertEqual(image_field.default, 'products/product_default.png')
