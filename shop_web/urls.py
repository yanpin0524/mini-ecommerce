from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic.base import RedirectView

from shop_web.views.auth_views import SignIn, SignUp
from shop_web.views.checkout_views import Checkout, CheckoutResult, CheckoutServerReturn
from shop_web.views.order_views import OrderDetail, OrderList
from shop_web.views.shop_views import CartAdd, CartList, CartRemove, ProductDetail, ProductList

urlpatterns = [
    path('products/<int:product_id>/', ProductDetail.as_view(), name='product-detail'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('cart/<int:product_id>/add/', CartAdd.as_view(), name='cart-add'),
    path('cart/<int:product_id>/remove/', CartRemove.as_view(), name='cart-remove'),
    path('cart/', CartList.as_view(), name='cart-list'),
    path('orders/<str:order_no>/', OrderDetail.as_view(), name='order-detail'),
    path('orders/', OrderList.as_view(), name='order-list'),
    path('checkout/return/', CheckoutServerReturn.as_view(), name='checkout-return'),
    path('checkout/result/', CheckoutResult.as_view(), name='checkout-result'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', RedirectView.as_view(pattern_name='product-list')),
]
