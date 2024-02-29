from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to="products", null=False, blank=False)


class CartItem(models.Model):  # 購物車中的商品
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)

    class Meta:
        unique_together = ("user_id", "product_id")


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_status = models.BooleanField(default=False)  # False = Not Delivered, True = Delivered


class OrderItem(models.Model):  # 訂單中的商品
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)

    class Meta:
        unique_together = ("order_id", "product_id")
