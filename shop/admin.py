from django.contrib import admin

from .models import CartItem, Order, OrderItem, Product, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'user', 'delivery_status', 'total')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'product')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
