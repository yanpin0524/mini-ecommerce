from django.shortcuts import render

from shop.models import Product


def shop_page(request):
    products = Product.objects.all()

    return render(request, 'shop.html', {'products': products})
