import os
import json
import io
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from PIL import Image
from shop.models import User, Product


class TestProductEndpoints(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            email="admin@gmail.com", password="admin123"
        )
        cls.normal_user = User.objects.create_user(
            email="user@gmail.com", password="user123"
        )

        # create a image for SimpleUploadedFile
        image = Image.new("RGB", (100, 100))
        cls.image_file = io.BytesIO()
        image.save(cls.image_file, "JPEG")  # save the image in memory
        cls.image_file.name = "image.jpg"
        cls.image_file.seek(0)

        cls.image = SimpleUploadedFile(
            name="image.jpg",
            content=cls.image_file.read(),
            content_type="image/jpeg",
        )

        cls.product = Product.objects.create(
            name="product1",
            price=100,
            description="This is product1's description.",
            image=cls.image,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        self.image_file.seek(0)

    def test_get_products(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_get_single_product(self):
        response = self.client.get(f"/api/products/{self.product.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["name"], "product1")

    def test_create_product(self):
        self.image2 = SimpleUploadedFile(
            name="image2.jpg",
            content=self.image_file.read(),
            content_type="image/jpeg",
        )

        data = {
            "name": "product2",
            "price": 200,
            "description": "This is product2's description.",
            "image": self.image2,
        }

        response = self.client.post("/api/products/", data, format="multipart")

        os.remove(f"images/products/{self.image2.name}")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_invalid_data(self):
        response = self.client.post("/api/products/", data={}, format="multipart")

        self.assertEqual(response.status_code, 400)

    def test_create_product_as_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.post("/api/products/", data={})
        self.assertEqual(response.status_code, 403)

    def test_update_product(self):
        data = {
            "name": "product1",
            "price": 150,
            "description": "This is product1's description.",
        }

        response = self.client.patch(
            f"/api/products/{self.product.id}/", data, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["price"], "150.00")

    def test_update_product_as_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.patch(f"/api/products/{self.product.id}/", data={})
        self.assertEqual(response.status_code, 403)

    def test_delete_product(self):
        image3 = SimpleUploadedFile(
            name="image3.jpg",
            content=self.image_file.read(),
            content_type="image/jpeg",
        )

        product_for_deletion = Product.objects.create(
            name="product_for_deletion",
            price=10,
            description="delete me!",
            image=image3,
        )
        response = self.client.delete(f"/api/products/{product_for_deletion.id}/")

        os.remove(f"images/products/{image3.name}")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 1)

    def test_delete_product_as_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)

        response = self.client.delete(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, 403)

    @classmethod
    def tearDownClass(cls):
        os.remove(f"images/products/{cls.image.name}")

        cls.image_file.close()
