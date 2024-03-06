from django.contrib import admin
from .models import User, Product, CartItem, Order, OrderItem

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)