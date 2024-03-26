import json
import os
import io
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from PIL import Image
from shop.models import User, Product, CartItem


class TestCartEndpoints(TestCase):

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

        cls.image_file.seek(0)
        cls.image2 = SimpleUploadedFile(
            name="image2.jpg",
            content=cls.image_file.read(),
            content_type="image/jpeg",
        )

        cls.product = Product.objects.create(
            name="Meteor Dark Ink Pen",
            price=9.99,
            description="An elegant dark ink pen with a smooth writing experience, suitable for daily use or as a gift.",
            image=cls.image,
        )

        cls.product2 = Product.objects.create(
            name="Star Wars Limited Edition T-shirt",
            price=59.99,
            description="A limited edition T-shirt themed around Star Wars, made from comfortable fabric, perfect for Star Wars fans to collect.",
            image=cls.image2,
        )

        cls.cart_item = CartItem.objects.create(
            user=cls.normal_user,
            product=cls.product,
            quantity=2,
        )

        cls.cart_item2 = CartItem.objects.create(
            user=cls.superuser,
            product=cls.product,
            quantity=3,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.normal_user)

    def test_get_my_cart(self):
        response = self.client.get("/api/cart/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_add_to_my_cart(self):
        data = {
            "product_id": self.product2.id,
            "quantity": 5,
        }

        response = self.client.post("/api/cart/", data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.content)["user"]["id"], self.normal_user.id
        )
        self.assertEqual(
            json.loads(response.content)["product"]["id"], self.product2.id
        )
        self.assertEqual(json.loads(response.content)["quantity"], 5)

    def test_update_quantity(self):
        data = {
            "quantity": 10,
        }

        response = self.client.patch("/api/cart/1/quantity/", data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["quantity"], 10)

    def test_clear_my_cart(self):
        print(CartItem.objects.all())
        response = self.client.delete("/api/cart/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(CartItem.objects.filter(user_id=self.normal_user.id).exists())

    def test_remove_single_cart_item(self):
        id = self.cart_item.id
        response = self.client.delete(f"/api/cart/{id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(CartItem.objects.filter(id=id).exists())

    @classmethod
    def tearDownClass(cls):
        CartItem.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

        os.remove(f"images/products/{cls.image.name}")
        os.remove(f"images/products/{cls.image2.name}")
        cls.image_file.close()
