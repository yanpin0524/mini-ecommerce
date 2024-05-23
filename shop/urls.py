from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

from shop.views import cart_views, order_views, product_views

urlpatterns = [
    path('products/', product_views.ProductView.as_view()),
    path('products/<int:pk>/', product_views.SingleProductView.as_view()),
    path('cart/', cart_views.CartItemView.as_view()),
    path('cart/<int:pk>/', cart_views.SingleCartItemView.as_view()),
    path('cart/<int:pk>/quantity/', cart_views.CartItemQuantityView.as_view()),
    path('orders/', order_views.OrderView.as_view()),
    path('orders/<int:pk>/', order_views.SingleOrderView.as_view()),
    path('orders/<int:pk>/status/', order_views.OrderDeliveryStatusView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
]
