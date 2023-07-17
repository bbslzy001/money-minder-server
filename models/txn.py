# money-minder-server\models\txn.py

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Txn(db.Model):
    txnId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    txnDateTime = db.Column(db.String(100))
    txnType = db.Column(db.String(100))
    txnCpty = db.Column(db.String(100))
    prodDesc = db.Column(db.String(100))
    incOrExp = db.Column(db.String(100))
    txnAmount = db.Column(db.Float)
    payMethod = db.Column(db.String(100))
    txnStatus = db.Column(db.String(100))
    billId = db.Column(db.Integer, db.ForeignKey('bill.billId', ondelete='CASCADE'))

    def __init__(self, txnDateTime, txnType, txnCpty, prodDesc, incOrExp, txnAmount, payMethod, txnStatus, billId):
        self.txnDateTime = txnDateTime
        self.txnType = txnType
        self.txnCpty = txnCpty
        self.prodDesc = prodDesc
        self.incOrExp = incOrExp
        self.txnAmount = txnAmount
        self.payMethod = payMethod
        self.txnStatus = txnStatus
        self.billId = billId
