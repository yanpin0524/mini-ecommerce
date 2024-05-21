import os
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from shop.models import CartItem, Order, OrderItem
from shop_web.services.ecpay_service import ECPayAllInOne

load_dotenv()


@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def post(self, request):
        cart = CartItem.objects.filter(user=request.user)
        if not cart.exists():
            return redirect('cart-list')

        cart_total = sum([item.total for item in cart])

        item_name = ''
        for item in cart:
            item_name += f'{item.product.name}#'

        host = os.getenv('HOST', 'http://localhost:8000')
        ecpay = ECPayAllInOne(
            MerchantID=os.getenv('MERCHANTID'),
            HashKey=os.getenv('HASHKEY'),
            HashIV=os.getenv('HASHIV'),
            ReturnURL=f'{host}{reverse("checkout-return")}',
            OrderResultURL=f'{host}{reverse("checkout-result")}',
        )

        return HttpResponse(
            ecpay.create_order(
                TradeDesc='Test Order',
                ItemName=item_name,
                TotalAmount=cart_total,
                UserId=str(request.user.id),
            )
        )


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutServerReturn(View):
    def post(self, request):
        ecpay_payment_sdk = ECPayAllInOne(
            MerchantID=os.getenv('MERCHANTID'),
            HashKey=os.getenv('HASHKEY'),
            HashIV=os.getenv('HASHIV'),
        ).ecpay_payment_sdk

        # 確認是由綠界送來的資料
        post_data = request.POST.dict()
        received_check_mac_value = post_data.get('CheckMacValue')
        calculated_check_mac_value = ecpay_payment_sdk.generate_check_value(post_data)

        if received_check_mac_value == calculated_check_mac_value:
            return HttpResponse('1|OK')

        return HttpResponse('0|Fail')


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutResult(View):
    def post(self, request):
        ecpay_payment_sdk = ECPayAllInOne(
            MerchantID=os.getenv('MERCHANTID'),
            HashKey=os.getenv('HASHKEY'),
            HashIV=os.getenv('HASHIV'),
        ).ecpay_payment_sdk

        post_data = request.POST.dict()

        order_date = datetime.strptime(post_data.get('TradeDate'), '%Y/%m/%d %H:%M:%S')
        print(order_date, type(order_date))

        received_check_mac_value = post_data.get('CheckMacValue')
        calculated_check_mac_value = ecpay_payment_sdk.generate_check_value(post_data)

        return_code = post_data.get('RtnCode')

        if received_check_mac_value == calculated_check_mac_value and return_code == '1':
            order_no = post_data.get('MerchantTradeNo')

            if Order.objects.filter(order_no=order_no).exists():
                return render(request, 'checkout_result.html', {'order_detail': post_data})

            user_id = int(post_data.get('CustomField1'))
            total = post_data.get('TradeAmt')
            created_at = datetime.strptime(post_data.get('TradeDate'), '%Y/%m/%d %H:%M:%S')

            order = Order.objects.create(
                user_id=user_id, order_no=order_no, total=total, created_at=created_at
            )
            order_items = []
            cart = CartItem.objects.filter(user_id=user_id)

            for item in cart:
                order_items.append(
                    OrderItem(order=order, product=item.product, quantity=item.quantity)
                )

            OrderItem.objects.bulk_create(order_items)
            cart.delete()

        return render(request, 'checkout_result.html', {'order_detail': post_data})
