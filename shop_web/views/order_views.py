from django.contrib.auth.decorators import login_required
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View

from shop.models import Order, OrderItem


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class OrderDetail(View):
    def get(self, request, order_no):
        order = get_object_or_404(Order, order_no=order_no, user=request.user)
        order_items = OrderItem.objects.filter(order=order)

        return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})
