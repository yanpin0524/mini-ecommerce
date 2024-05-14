from django.contrib.auth.views import LogoutView
from django.urls import path

from shop_web.views import auth_views, shop_views

urlpatterns = [
    path('shop/<int:product_id>/', shop_views.ProductDetailView.as_view(), name='product_detail'),
    path('shop/', shop_views.ShopView.as_view(), name='shop_page'),
    path('my-cart/', shop_views.MyCartView.as_view(), name='my_cart'),
    path('sign-in/', auth_views.SignInView.as_view(), name='sign_in'),
    path('sign-up/', auth_views.SignUpView.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(next_page='/sign-in/'), name='logout'),
    path('', shop_views.ShopView.as_view()),
]
