from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, DecimalField, SubmitField, HiddenField, IntegerField, StringField
from wtforms.validators import InputRequired, NumberRange, Length
from invoice.model import CURRENCY

class TransactionForm(FlaskForm):
    amount = DecimalField(label="Amount", 
                            validators=[InputRequired(), NumberRange(min=0.01)])
    description = TextAreaField(label="Description", 
                            validators=[InputRequired(), Length(min=2, max=255)])
    currency = SelectField(label="Currency", choices=[c[0:2] for c in CURRENCY])
    submit = SubmitField("Pay")


class PayForm(FlaskForm):
    amount = HiddenField()
    description = HiddenField()
    currency = HiddenField()
    shop_id = HiddenField()
    shop_order_id = HiddenField()
    sign = HiddenField()
    submit = SubmitField("Confirm")
    action = StringField()

class InvoiceForm(FlaskForm):
    m_curorderid = IntegerField()
    m_historyid = IntegerField()
    m_historytm = IntegerField()
    referer = StringField()
    action = StringField()
    method = StringField()
    submit = SubmitField("Confirm")
    lang = StringField()