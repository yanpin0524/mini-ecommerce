import os
from pprint import pprint

from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from shop_web.services.ecpay_service import ECPayAllInOne

load_dotenv()


class Checkout(View):
    def get(self, request):
        host = os.getenv('HOST', 'http://localhost:8000')
        ecpay = ECPayAllInOne(
            MerchantID='2000132',  # 測試用帳號
            HashKey='5294y06JbISpM5x9',
            HashIV='v77hoKGq4kWxNNIS',
            ReturnURL=f'{host}{reverse("checkout-return")}',
            ClientBackURL=f'{host}{reverse("cart-list")}',
            OrderResultURL=f'{host}{reverse("checkout-client-back")}',
        )

        return HttpResponse(
            ecpay.create_order(TradeDesc='測試交易', ItemName='我是測試用商品', TotalAmount=150)
        )


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutReturn(View):
    def post(self, request):
        ecpay_payment_sdk = ECPayAllInOne(
            MerchantID='2000132',  # 測試用帳號
            HashKey='5294y06JbISpM5x9',
            HashIV='v77hoKGq4kWxNNIS',
        ).ecpay_payment_sdk

        post_data = request.POST.dict()
        received_check_mac_value = post_data.get('CheckMacValue')
        calculated_check_mac_value = ecpay_payment_sdk.generate_check_value(post_data)

        if received_check_mac_value == calculated_check_mac_value:
            return HttpResponse('1|OK')

        return HttpResponse('0|Fail')


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutClientBack(View):
    def post(self, request):
        ecpay_payment_sdk = ECPayAllInOne(
            MerchantID='2000132',  # 測試用帳號
            HashKey='5294y06JbISpM5x9',
            HashIV='v77hoKGq4kWxNNIS',
        ).ecpay_payment_sdk

        post_data = request.POST.dict()
        received_check_mac_value = post_data.get('CheckMacValue')
        return_message = post_data.get('RtnMsg')
        return_code = post_data.get('RtnCode')

        calculated_check_mac_value = ecpay_payment_sdk.generate_check_value(post_data)

        if received_check_mac_value == calculated_check_mac_value and return_code == '1':
            pprint(post_data)

        return HttpResponse(return_message)
