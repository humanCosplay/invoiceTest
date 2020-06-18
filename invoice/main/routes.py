from flask import render_template, request, flash, redirect, url_for, Blueprint
from invoice.forms import TransactionForm
from invoice.transactions import create_payment_method

main = Blueprint('main', __name__)

@main.route("/payment/<shop_order_id>", methods=["GET", "POST"])
def handle_payment(shop_order_id):
    form = TransactionForm()
    if form.validate_on_submit():
        method = create_payment_method(form.amount.data, form.currency.data, form.description.data, shop_order_id)
        if method:
            return method.process_payment(form)
        else:
            flash('Payment request failed!', 'danger')
        return redirect(url_for('main.handle_payment', shop_order_id=shop_order_id))
    return render_template("index.html", form=form)