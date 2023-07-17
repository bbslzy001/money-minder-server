# money-minder-server\models\txn.py

from models import db


class Txn(db.Model):
    txn_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    txn_date_time = db.Column(db.String(100))
    txn_type = db.Column(db.String(100))
    txn_cpty = db.Column(db.String(100))
    prod_desc = db.Column(db.String(100))
    inc_or_exp = db.Column(db.String(100))
    txn_amount = db.Column(db.Float)
    pay_method = db.Column(db.String(100))
    txn_status = db.Column(db.String(100))
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.billId', ondelete='CASCADE'))

    def __init__(self, txn_date_time, txn_type, txn_cpty, prod_desc, inc_or_exp, txn_amount, pay_method, txn_status, bill_id):
        self.txn_date_time = txn_date_time
        self.txn_type = txn_type
        self.txn_cpty = txn_cpty
        self.prod_desc = prod_desc
        self.inc_or_exp = inc_or_exp
        self.txn_amount = txn_amount
        self.pay_method = pay_method
        self.txn_status = txn_status
        self.bill_id = bill_id
