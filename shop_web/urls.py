from django.urls import path

from shop_web.views import shop_views

urlpatterns = [
    path('product/<int:product_id>/', shop_views.product_detail, name='product_detail'),
    path('shop/', shop_views.shop_page, name='shop_page'),
    path('', shop_views.shop_page),
]
