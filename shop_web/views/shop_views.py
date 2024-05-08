from django.shortcuts import get_object_or_404, render

from shop.models import Product


def shop_page(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'product_detail.html', {'product': product})
