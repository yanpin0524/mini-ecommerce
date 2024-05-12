from django.urls import path

from shop_web.views import auth_views, shop_views

urlpatterns = [
    path('product/<int:product_id>/', shop_views.product_detail, name='product_detail'),
    path('shop/', shop_views.shop_page, name='shop_page'),
    path('sign-in/', auth_views.SignInView.as_view(), name='sign_in'),
    path('sign-up/', auth_views.SignUpView.as_view(), name='sign_up'),
    path('', shop_views.shop_page),
]
