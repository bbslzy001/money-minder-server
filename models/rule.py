# money-minder-server\models\rule.py

from models import db


class Rule(db.Model):
    __tablename__ = 'rule'

    rule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    origin_txn_type = db.Column(db.String(100))
    txn_cpty = db.Column(db.String(100))
    prod_desc = db.Column(db.String(100))
    txn_type_id = db.Column(db.Integer, db.ForeignKey('txn_type.txn_type_id'))

    # txns = db.relationship("Txn", cascade="all, delete, delete-orphan")  # 不操作 / 将对应的Txn中的rule_id字段变更为1

    def __init__(self, origin_txn_type, txn_cpty, prod_desc, txn_type_id):
        self.origin_txn_type = origin_txn_type
        self.txn_cpty = txn_cpty
        self.prod_desc = prod_desc
        self.txn_type_id = txn_type_id
