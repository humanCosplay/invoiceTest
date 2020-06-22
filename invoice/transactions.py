import requests
from hashlib import sha256
from flask import flash, current_app, redirect, render_template
from invoice.model import Payments, CURRENCY, log_transaction
from invoice.forms import PayForm, InvoiceForm
from invoice import db


class Transaction:

    def __init__(self, amount, description, shop_order_id):
        self.amount = amount
        self.shop_order_id = shop_order_id
        self.description = description

    def process_paymnet(self):
        pass

    def make_seed_for_sign(self):
        return {}

    def make_secret(self, nessecary_request):
        if nessecary_request == {}: 
            return None

        hashable_request = ":".join((str(value) for _, value in sorted(nessecary_request.items())))
        hashable_request = hashable_request + current_app.config['SECRET_KEY']
        return sha256(hashable_request.encode()).hexdigest()

    def str_amount(self):
        return f"{self.amount:.2f}"


class Pay(Transaction):
    template = "eu_pay.html"

    def __init__(self, amount, description, shop_order_id):
        super().__init__(amount, description, shop_order_id)
        self.currency = CURRENCY[0][2]
    
    def create_confirmation_form(self):
        confirmation_form = PayForm(shop_id=current_app.config["SHOP_ID"],
                                shop_order_id=self.shop_order_id,
                                description=self.description,
                                action="https://pay.piastrix.com/ru/pay")

        confirmation_form.sign.data = self.make_secret(self.make_seed_for_sign())
        confirmation_form.amount.data = self.str_amount()
        confirmation_form.currency.data = self.currency
        return confirmation_form

    def process_payment(self, external_form):
        log_transaction(external_form.amount.data, 
                        external_form.currency.data, 
                        external_form.description.data)
        return render_template(self.template, 
                                form=external_form, 
                                confirmation_form=self.create_confirmation_form())
    
    def make_seed_for_sign(self):
        return {"amount": self.str_amount(),
                "currency": self.currency,
                "shop_id": current_app.config["SHOP_ID"],
                "shop_order_id": self.shop_order_id}


class Bill(Transaction):
    template = "index.html"

    def __init__(self, amount, description, shop_order_id):
        super().__init__(amount, description, shop_order_id)
        self.currency = CURRENCY[1][2]
    
    def get_api_bill_response(self):
        json_request = self.make_seed_for_sign()
        sign = self.make_secret(json_request)
        json_request["sign"] = sign
        response = requests.post("https://core.piastrix.com/bill/create", json=json_request)

        if response.status_code != 200:
            return None

        json_data = response.json()
        if json_data['error_code'] != 0:
            return None

        return json_data

    def process_payment(self, external_form):
        json_data = self.get_api_bill_response()
        if json_data:
            log_transaction(external_form.amount.data, 
                            external_form.currency.data, 
                            external_form.description.data)
            return redirect(json_data['url'])

        flash('Payment request failed!', 'danger')
        return render_template(self.template, form=external_form)
    
    def make_seed_for_sign(self):
        return {"shop_amount": self.str_amount(),
                "shop_currency": self.currency,
                "payer_currency": self.currency,
                "shop_id": current_app.config["SHOP_ID"],
                "shop_order_id": self.shop_order_id}


class Invoice(Transaction):
    template = "ru_invoice.html"

    def __init__(self, amount, description, shop_order_id):
        super().__init__(amount, description, shop_order_id)
        self.currency = CURRENCY[2][2]
    
    def process_payment(self, external_form):
        json_response = self.get_api_invoice_response()
        if json_response:
            log_transaction(external_form.amount.data, 
                            external_form.currency.data, 
                            external_form.description.data)
            return render_template(self.template, 
                                   form=external_form, 
                                   confirmation_form=self.create_confirmation_form())
        
        flash('Payment request failed!', 'danger')
        return render_template("index.html", form=external_form)

    def get_api_invoice_response(self):
        json_request = self.make_seed_for_sign()
        sign = self.make_secret(json_request)
        json_request["sign"] = sign
        json_request["amount"] = str(json_request["amount"])
        response = requests.post("https://core.piastrix.com/bill/create", json=json_request)

        if response.status_code != 200:
            return None
        
        json_response = response.json()
        if json_response['error_code'] != 0:
            return None

        return json_response

    def create_confirmation_form(self, response):
        data = response['data']
        data['url'] = response['url']
        confirmation_form = InvoiceForm(**data)
        return confirmation_form
    
    def make_seed_for_sign(self):
        return {"amount": self.str_amount(),
                "currency": self.currency,
                "payway": "payeer_rub",
                "shop_id": current_app.config["SHOP_ID"],
                "shop_order_id": self.shop_order_id}



def create_payment_method(amount, currency, description, shop_order_id):
    if currency in CURRENCY[0]:
        return Pay(amount, description, shop_order_id)
    elif currency in CURRENCY[1]:
        return Bill(amount, description, shop_order_id)
    elif currency in CURRENCY[2]:
        return Invoice(amount, description, shop_order_id)
    else:
        return None