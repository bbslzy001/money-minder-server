# money-minder-server\services\txn_service.py

from models import db
from models.txn import Txn


def add_txn(data):
    new_txn = Txn(
        txn_date_time=data['txnDateTime'],
        txn_type=data['txnType'],
        txn_cpty=data['txnCpty'],
        prod_desc=data['prodDesc'],
        inc_or_exp=data['incOrExp'],
        txn_amount=data['txnAmount'],
        pay_method=data['payMethod'],
        txn_status=data['txnStatus'],
        bill_id=data['billId']
    )
    db.session.add(new_txn)
    db.session.commit()
    txn_id = new_txn.txn_id  # 获取自增ID
    return {'message': 'Transaction added successfully', 'id': txn_id}


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
    txn.txn_date_time = data.get('txnDateTime', txn.txn_date_time)
    txn.txn_type = data.get('txnType', txn.txn_type)
    txn.txn_cpty = data.get('txnCpty', txn.txn_cpty)
    txn.prod_desc = data.get('prodDesc', txn.prod_desc)
    txn.inc_or_exp = data.get('incOrExp', txn.inc_or_exp)
    txn.txn_amount = data.get('txnAmount', txn.txn_amount)
    txn.pay_method = data.get('payMethod', txn.pay_method)
    txn.txn_status = data.get('txnStatus', txn.txn_status)
    txn.bill_id = data.get('billId', txn.bill_id)
    db.session.commit()
    return {'message': 'Transaction updated successfully'}


def get_txns():
    txns = Txn.query.all()
    result = []
    for txn in txns:
        result.append({
            'txnId': txn.txn_id,
            'txnDateTime': txn.txn_date_time,
            'txnType': txn.txn_type,
            'txnCpty': txn.txn_cpty,
            'prodDesc': txn.prod_desc,
            'incOrExp': txn.inc_or_exp,
            'txnAmount': txn.txn_amount,
            'payMethod': txn.pay_method,
            'txnStatus': txn.txn_status,
            'billId': txn.bill_id
        })
    return {'message': 'Transaction gotten successfully', 'result': result}
