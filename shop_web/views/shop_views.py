from django.shortcuts import render

from shop.models import Product


def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(request, 'product_detail.html', {'product': product})
