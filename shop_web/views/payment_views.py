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
            MerchantID=os.getenv('MERCHANTID'),
            HashKey=os.getenv('HASHKEY'),
            HashIV=os.getenv('HASHIV'),
            ReturnURL=f'{host}{reverse("checkout-return")}',
            ClientBackURL=f'{host}{reverse("cart-list")}',
            OrderResultURL=f'{host}{reverse("checkout-client-back")}',
        )

        return HttpResponse(
            ecpay.create_order(TradeDesc='測試交易', ItemName='我是測試用商品', TotalAmount=150)
        )


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutReturn(View):
    # ? 似乎沒有用到
    def post(self, request):
        pprint(request.POST.dict())

        ecpay = ECPayAllInOne(
            MerchantID=os.getenv('ECPAY_MERCHANT_ID'),
            HashKey=os.getenv('ECPAY_HASH_KEY'),
            HashIV=os.getenv('ECPAY_HASH_IV'),
        ).ecpay_payment_sdk

        res = request.POST.dict()
        back_check_mac_value = request.POST.get('CheckMacValue')
        check_mac_value = ecpay.generate_check_value(res)

        if back_check_mac_value == check_mac_value:
            return HttpResponse('0|Fail')

        return HttpResponse('0|Fail')


@method_decorator(csrf_exempt, name='dispatch')
class CheckoutClientBack(View):
    def post(self, request):
        ecpay = ECPayAllInOne(
            MerchantID=os.getenv('ECPAY_MERCHANT_ID'),
            HashKey=os.getenv('ECPAY_HASH_KEY'),
            HashIV=os.getenv('ECPAY_HASH_IV'),
        ).ecpay_payment_sdk

        res = request.POST.dict()
        back_check_mac_value = request.POST.get('CheckMacValue')
        # order_id = request.POST.get('MerchantTradeNo')
        return_msg = request.POST.get('RtnMsg')
        return_code = request.POST.get('RtnCode')

        check_mac_value = ecpay.generate_check_value(res)
        pprint(res)
        if back_check_mac_value == check_mac_value and return_code == '1':
            # save to order model
            return HttpResponse(return_msg)

        return HttpResponse(return_msg)

    def get(self, request):
        return HttpResponse('<h1>交易完成</h1>')
