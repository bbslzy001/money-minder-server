# money-minder-server\services\txn_service.py

from models import db
from models.txn import Txn


def add_txn(data):
    new_txn = Txn(
        txnDateTime=data['txnDateTime'],
        txnType=data['txnType'],
        txnCpty=data['txnCpty'],
        prodDesc=data['prodDesc'],
        incOrExp=data['incOrExp'],
        txnAmount=data['txnAmount'],
        payMethod=data['payMethod'],
        txnStatus=data['txnStatus'],
        billId=data['billId']
    )
    db.session.add(new_txn)
    db.session.commit()
    txn_id = new_txn.txnId  # 获取自增ID
    return {'message': 'Transaction added successfully', 'txnId': txn_id}


def delete_txn(txn_id):
    txn = Txn.query.get(txn_id)
    if not txn:
        return {'error': 'Transaction not found'}
    db.session.delete(txn)
    db.session.commit()
    return {'message': 'Transaction deleted successfully'}


def update_txn(txn_id, data):
    txn = Txn.query.get(txn_id)
    if not txn:
        return {'error': 'Transaction not found'}
    txn.txnDateTime = data.get('txnDateTime', txn.txnDateTime)
    txn.txnType = data.get('txnType', txn.txnType)
    txn.txnCpty = data.get('txnCpty', txn.txnCpty)
    txn.prodDesc = data.get('prodDesc', txn.prodDesc)
    txn.incOrExp = data.get('incOrExp', txn.incOrExp)
    txn.txnAmount = data.get('txnAmount', txn.txnAmount)
    txn.payMethod = data.get('payMethod', txn.payMethod)
    txn.txnStatus = data.get('txnStatus', txn.txnStatus)
    txn.billId = data.get('billId', txn.billId)
    db.session.commit()
    return {'message': 'Transaction updated successfully'}


def get_txns():
    txns = Txn.query.all()
    result = []
    for txn in txns:
        result.append({
            'txnId': txn.txnId,
            'txnDateTime': txn.txnDateTime,
            'txnType': txn.txnType,
            'txnCpty': txn.txnCpty,
            'prodDesc': txn.prodDesc,
            'incOrExp': txn.incOrExp,
            'txnAmount': txn.txnAmount,
            'payMethod': txn.payMethod,
            'txnStatus': txn.txnStatus,
            'billId': txn.billId
        })
    return result
