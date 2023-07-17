# money-minder-server\models\bill.py

from models import db


class Bill(db.Model):
    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_name = db.Column(db.String(100))

    def __init__(self, bill_name):
        self.bill_name = bill_name
