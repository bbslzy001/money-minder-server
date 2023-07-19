# money-minder-server\models\bill.py

from models import db


class Bill(db.Model):
    __tablename__ = 'bill'

    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_name = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    bill_type = db.Column(db.String(100))

    txns = db.relationship("Txn", cascade="all, delete, delete-orphan")  # 一对多关系，代码级联删除

    def __init__(self, bill_name, start_date, end_date, bill_type):
        self.bill_name = bill_name
        self.start_date = start_date
        self.end_date = end_date
        self.bill_type = bill_type

