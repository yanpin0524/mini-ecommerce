import json
import os
import io
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from PIL import Image
from shop.models import User, Product, CartItem, Order, OrderItem


class TestOrderEndpoints(TestCase):

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

    def setUp(self):
        self.cart_item = CartItem.objects.create(
            user=self.normal_user,
            product=self.product,
            quantity=2,
        )

        self.cart_item2 = CartItem.objects.create(
            user=self.normal_user,
            product=self.product2,
            quantity=1,
        )

        self.order = Order.objects.create(user=self.normal_user)

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=5,
        )

        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            price=self.product2.price,
            quantity=10,
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.normal_user)

    def tearDown(self):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        CartItem.objects.all().delete()

    def test_get_orders(self):
        response = self.client.get("/api/orders/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_get_order_details(self):
        response = self.client.get(f"/api/orders/{self.order.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)["order_items"]), 2)

    def test_get_order_details_not_belong_you(self):
        order_from_other_user = Order.objects.create(user=self.superuser)
        response = self.client.get(f"/api/orders/{order_from_other_user.id}/")

        self.assertEqual(response.status_code, 403)

    def test_create_order(self):
        response = self.client.post("/api/orders/")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Order.objects.filter(user=self.normal_user)), 2)
        self.assertEqual(len(CartItem.objects.filter(user=self.normal_user)), 0)

    def test_update_order_status(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.patch(
            f"/api/orders/{self.order.id}/status/", {"delivered": "True"}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)["delivered"])

    def test_update_order_status_with_non_admin(self):
        response = self.client.patch(
            f"/api/orders/{self.order.id}/status/", {"delivered": "True"}, format="json"
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_order(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.delete(f"/api/orders/{self.order.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Order.objects.filter(id=self.order.id)), 0)
        self.assertEqual(len(OrderItem.objects.filter(order_id=self.order.id)), 0)

    def test_delete_order_with_non_admin(self):
        response = self.client.delete(f"/api/orders/{self.order.id}/")

        self.assertEqual(response.status_code, 403)

    @classmethod
    def tearDownClass(cls):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        CartItem.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

        os.remove(f"images/products/{cls.image.name}")
        os.remove(f"images/products/{cls.image2.name}")

        cls.image_file.close()
