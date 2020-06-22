from flask import Flask
from flask_testing import TestCase
from invoice.transactions import Transaction, Pay, Bill


class MakeSignTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["SECRET_KEY"] = "SecretKey01"
        app.config["TESTING"] = True
        return app

    def setUp(self):
        self.tr = Transaction(0, "", 0)
    
    def test_raise_error_on_empty_request(self):
        sign = self.tr.make_secret({})
        assert sign is None

    def test_process_unsorted_request(self):
        request = {"shop_id":5, "payway":"payeer_rub", "amount":12.34, "currency":"643", "shop_order_id":4126}
        sign = self.tr.make_secret(request)
        assert sign == "9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1"

    def test_process_sorted_request(self):
        request = {"amount":12.34, "currency":"643", "payway":"payeer_rub", "shop_id":5, "shop_order_id":4126}
        sign = self.tr.make_secret(request)
        assert sign == "9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1"
 
    def test_process_sorted_request_stringified(self):
        request = {"amount":"12.34", "currency":"643", "payway":"payeer_rub", "shop_id":5, "shop_order_id":4126}
        sign = self.tr.make_secret(request)
        assert sign == "9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1"\

    def test_process_sorted_request_stringified_int(self):
        request = {"amount":"12.00", "currency":"643", "payway":"payeer_rub", "shop_id":5, "shop_order_id":4126}
        sign = self.tr.make_secret(request)
        assert sign == "a53e5e2f6592e3c0d14cef57b15009350c86a2e0edf76cd06dfc49002c92ab9d"

    def test_process_sorted_request_int(self):
        request = {"amount":12, "currency":"643", "payway":"payeer_rub", "shop_id":5, "shop_order_id":4126}
        sign = self.tr.make_secret(request)
        assert sign != "a53e5e2f6592e3c0d14cef57b15009350c86a2e0edf76cd06dfc49002c92ab9d"

    
class PayTests(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["SECRET_KEY"] = "SecretKey01"
        app.config["TESTING"] = True
        app.config["SHOP_ID"] = 5
        return app

    def setUp(self):
        self.pay = Pay(111, "Test", 1)
    
    def test_seed_for_sign(self):
        seed = self.pay.make_seed_for_sign()

        assert seed == {"amount": "111.00", 
                        "currency": 978, 
                        "shop_id": self.app.config["SHOP_ID"],
                        "shop_order_id": 1}

    def test_confirmation_form(self):
        form = self.pay.create_confirmation_form()
        
        assert form.amount.data        == "111.00"
        assert form.currency.data      == 978
        assert form.sign.data          == "a96f80d1a8a516e4e2b7528e1c300472f4af110f9f145569df7566654a94b4bf"
        assert form.shop_id.data       == self.app.config["SHOP_ID"]
        assert form.shop_order_id.data == 1
        assert form.action.data        == "https://pay.piastrix.com/ru/pay"


class BillTests(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["SECRET_KEY"] = "SecretKey01"
        app.config["TESTING"] = True
        app.config["SHOP_ID"] = 5
        return app

    def setUp(self):
        self.bill = Bill(111, "Test", 1)
    
    def test_seed_for_sign(self):
        seed = self.bill.make_seed_for_sign()
        assert seed == {"shop_amount": "111.00", 
                        "shop_currency": 840,
                        "payer_currency": 840,
                        "shop_id": self.app.config["SHOP_ID"],
                        "shop_order_id": 1}

    def test_request_params(self):
        params = self.bill.make_request_params()
        assert params == {"shop_amount": "111.00", 
                        "shop_currency": 840,
                        "payer_currency": 840,
                        "shop_id": self.app.config["SHOP_ID"],
                        "shop_order_id": 1,
                        "sign": "d9bbbbffdb55ce3e1d31198058b99be13a916dda823db04f9148ad5a182b369c",
                        "description": "Test"}