from django.urls import path

from shop_web.views import shop_views

urlpatterns = [
    path('', shop_views.shop_page, name='shop_page'),
]
