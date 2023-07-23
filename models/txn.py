# money-minder-server\models\txn.py

from models import db


class Txn(db.Model):
    __tablename__ = 'txn'

    txn_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    txn_date_time = db.Column(db.String(100))
    txn_cpty = db.Column(db.String(100))
    prod_desc = db.Column(db.String(100))
    inc_or_exp = db.Column(db.String(100))
    txn_amount = db.Column(db.Float)
    pay_method = db.Column(db.String(100))
    txn_status = db.Column(db.String(100))
    origin_txn_type = db.Column(db.String(100))  # 用于记录原始交易类型，方便后续修改规则时进行筛选
    txn_type_id = db.Column(db.Integer, db.ForeignKey('txn_type.txn_type_id'))
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.rule_id'), nullable=True)  # 存在未使用规则的交易记录
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.bill_id'))

    def __init__(self, txn_date_time, txn_cpty, prod_desc, inc_or_exp, txn_amount, pay_method, txn_status, origin_txn_type, txn_type_id, rule_id, bill_id):
        self.txn_date_time = txn_date_time
        self.txn_cpty = txn_cpty
        self.prod_desc = prod_desc
        self.inc_or_exp = inc_or_exp
        self.txn_amount = txn_amount
        self.pay_method = pay_method
        self.txn_status = txn_status
        self.origin_txn_type = origin_txn_type
        self.txn_type_id = txn_type_id
        self.rule_id = rule_id
        self.bill_id = bill_id
