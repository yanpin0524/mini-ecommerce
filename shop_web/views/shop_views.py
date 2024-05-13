from django.shortcuts import get_object_or_404, render
from django.views import View

from shop.models import Product


class ShopView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shop.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'product_detail.html', {'product': product})
