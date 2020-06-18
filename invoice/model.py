from invoice import db


CURRENCY = [("eur", "€", 978),
            ("usd", "$", 840),
            ("rub", "₽", 643)]


class Payments(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL(18,2), nullable=False)
    currency = db.Column(db.Enum(*[c[0] for c in CURRENCY], name="currency"))
    description = db.Column(db.String(255), nullable=False)
    commited = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"Transaction(id={self.id}, amount={self.amount} {self.currency}, commited={self.commited})"


def log_transaction(amount, currency, description):
    payment = Payments(amount=amount, currency=currency, description=description)
    db.session.add(payment)
    db.session.commit()