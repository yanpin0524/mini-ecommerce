from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from shop.models import CartItem, Product
from shop_web.forms.cart_forms import CartAddForm


class ProductList(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})


class ProductDetail(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm()

        if request.session.get('form_content'):
            form = CartAddForm(request.session.get('form_content'))

            del request.session['form_content']

        return render(request, 'product_detail.html', {'product': product, 'form': form})


class CartAdd(View):
    def post(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')

            cart_item, created = CartItem.objects.get_or_create(
                user=user, product=product, defaults={'quantity': 0}
            )

            cart_item.quantity += quantity
            cart_item.save()

        request.session['form_content'] = request.POST
        return redirect(request.META.get('HTTP_REFERER'))


class CartList(View):
    def get(self, request):
        cart = CartItem.objects.filter(user=request.user)
        cart_total = sum([item.total for item in cart])
        return render(request, 'cart_list.html', {'cart': cart, 'cart_total': cart_total})
