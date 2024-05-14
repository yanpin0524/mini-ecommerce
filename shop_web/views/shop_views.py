from django.shortcuts import get_object_or_404, render
from django.views import View

from shop.models import CartItem, Product
from shop_web.forms.cart_forms import CartAddForm


class ProductList(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})


class ProductDetail(View):
    def get(self, request, product_id, form=None):
        product = get_object_or_404(Product, id=product_id)

        if form is None:
            form = CartAddForm()

        return render(request, 'product_detail.html', {'product': product, 'form': form})


class CartAdd(View):
    def post(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)

        if CartItem.objects.filter(user=user, product=product).exists():
            # TODO: redirect to cart-edit path, then update quantity.
            form.add_error(None, 'Product already in cart!')

        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            CartItem.objects.create(user=user, product=product, quantity=quantity)

        return ProductDetail.get(self, request, product_id, form)


class CartList(View):
    def get(self, request):
        cart = CartItem.objects.filter(user=request.user)
        cart_total = sum([item.total for item in cart])
        return render(request, 'cart_list.html', {'cart': cart, 'cart_total': cart_total})
