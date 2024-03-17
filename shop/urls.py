from django.urls import path
import shop.views as views

urlpatterns = [
    path("products/", views.ProductView.as_view()),
    path("products/<int:pk>/", views.SingleProductView.as_view()),
    path("cart/", views.CartItemView.as_view()),
    path("cart/<int:pk>/quantity", views.CartItemQuantityView.as_view()),
    path("cart/<int:pk>/", views.SingleCartItemView.as_view()),
    path("orders/", views.OrderView.as_view()),
    path("orders/<int:pk>/", views.SingleOrderView.as_view()),
    path("orders/<int:pk>/status/", views.OrderDeliveryStatusView.as_view()),
]
