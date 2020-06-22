from flask import Flask
from flask_testing import TestCase
from invoice.transactions import Transaction


class MakeSignTest(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["SECRET_KEY"] = "SecretKey01"
        app.config["TESTING"] = True
        return app

    
    def test_raise_error_on_empty_request(self):
        tr = Transaction()
        sign = tr.make_secret({})
        assert sign is None

    def test_process_unsorted_request(self):
        tr = Transaction()
        request = {"shop_id":5, "payway":"payeer_rub", "amount":12.34, "currency":"643", "shop_order_id":4126}
        sign = tr.make_secret(request)
        assert sign == "9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1"

    def test_process_sorted_request(self):
        tr = Transaction()
        request = {"amount":12.34, "currency":"643", "payway":"payeer_rub", "shop_id":5, "shop_order_id":4126}
        sign = tr.make_secret(request)
        assert sign == "9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1"
 
    def test_process_sorted_request_stringified(self):
        tr = Transaction()
        request = {"amount":"12.34", "currency":"643", "payway":"payeer_rub", "shop_id":5, "shop_order_id":4126}
        sign = tr.make_secret(request)
        assert sign == "9cf003e3ad9da90ff00b06349b677261d5539f7e0540fb976c45537a141222c1"\

    def test_process_sorted_request_stringified_int(self):
        tr = Transaction()
        request = {"amount":"12.00", "currency":"643", "payway":"payeer_rub", "shop_id":5, "shop_order_id":4126}
        sign = tr.make_secret(request)
        assert sign == "a53e5e2f6592e3c0d14cef57b15009350c86a2e0edf76cd06dfc49002c92ab9d"

    def test_process_sorted_request_int(self):
        tr = Transaction()
        request = {"amount":12, "currency":"643", "payway":"payeer_rub", "shop_id":5, "shop_order_id":4126}
        sign = tr.make_secret(request)
        assert sign != "a53e5e2f6592e3c0d14cef57b15009350c86a2e0edf76cd06dfc49002c92ab9d"