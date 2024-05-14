from django.shortcuts import get_object_or_404, render
from django.views import View

from shop.models import CartItem, Product
from shop_web.forms.cart_forms import AddToCartForm


class ShopView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shop.html', {'products': products})


# If you want to create or edit products, please go to the Admin panel or use API.
class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = AddToCartForm()

        return render(request, 'product_detail.html', {'product': product, 'form': form})

    # Add product to cart
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = AddToCartForm(request.POST)

        if CartItem.objects.filter(user=request.user, product=product).exists():
            form.add_error('__all__', 'Product already in cart!')

        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')

            CartItem.objects.create(user=request.user, product=product, quantity=quantity)

        return render(request, 'product_detail.html', {'product': product, 'form': form})


class MyCartView(View):
    def get(self, request):
        cart = CartItem.objects.filter(user=request.user)
        cart_total = sum([item.total for item in cart])
        return render(request, 'my_cart.html', {'cart': cart, 'cart_total': cart_total})
