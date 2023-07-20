# money-minder-server\models\txn_type.py

from models import db


class TxnType(db.Model):
    __tablename__ = 'txn_type'

    txn_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    txn_type_name = db.Column(db.String(100))

    rules = db.relationship("Rule", cascade="all, delete, delete-orphan")  # 一对多关系，代码级联删除

    def __init__(self, txn_type_name):
        self.txn_type_name = txn_type_name
