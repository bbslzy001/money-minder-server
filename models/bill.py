# money-minder-server\models\bill.py

from models import db


class Bill(db.Model):
    __tablename__ = 'bill'

    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_name = db.Column(db.String(100))

    txns = db.relationship("Txn", cascade="all, delete, delete-orphan")  # 一对多关系，代码级联删除

    def __init__(self, bill_name):
        self.bill_name = bill_name
