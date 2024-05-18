import importlib.util
from datetime import datetime

spec = importlib.util.spec_from_file_location(
    'ecpay_payment_sdk', 'shop_web/services/ecpay_payment_sdk.py'
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ECPayAllInOne:
    def __init__(self, MerchantID, HashKey, HashIV, ReturnURL='', ClientBackURL=''):
        self.MerchantID = MerchantID
        self.HashKey = HashKey
        self.HashIV = HashIV
        self.ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID=self.MerchantID, HashKey=self.HashKey, HashIV=self.HashIV
        )

        self.ReturnURL = ReturnURL
        self.ClientBackURL = ClientBackURL

    def create_order(self, TradeDesc: str, ItemName: str, TotalAmount: int):
        order_params = {
            'MerchantTradeNo': datetime.now().strftime('NO%Y%m%d%H%M%S'),
            'MerchantTradeDate': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'PaymentType': 'aio',
            'TradeDesc': TradeDesc,
            'ItemName': ItemName,
            'TotalAmount': TotalAmount,
            'ReturnURL': self.ReturnURL,
            'ClientBackURL': self.ClientBackURL,
            'ChoosePayment': 'ALL',
            'EncryptType': 1,
        }

        try:
            ecpay_order_params = self.ecpay_payment_sdk.create_order(order_params)

            action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
            html = self.ecpay_payment_sdk.gen_html_post_form(action_url, ecpay_order_params)

            return html
        except Exception as error:
            print(f'An exception happened: {error}')
