from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User, Product, CartItem, Order, OrderItem


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    user_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "user", "product", "quantity", "user_id", "product_id"]


class CartItemQuantitySerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "quantity"]


class OrderSerializer(ModelSerializer):
    delivered = serializers.BooleanField(read_only=True, source="delivery_status")
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "delivered"]

class OrderDeliveryStatusSerializer(ModelSerializer):
    delivered = serializers.BooleanField(source="delivery_status")

    class Meta:
        model = Order
        fields = ["id", "delivered"]

class OrderItemSerializer(ModelSerializer):
    total = serializers.SerializerMethodField(method_name="get_total")

    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    order_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "price", "quantity", "total", "order_id", "product_id"]

    def get_total(self, obj):
        return obj.price * obj.quantity
