# money-minder-server\models\bill.py

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Bill(db.Model):
    billId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    billName = db.Column(db.String(100))

    def __init__(self, billName):
        self.billName = billName
