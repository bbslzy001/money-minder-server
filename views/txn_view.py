# money-minder-server\views\txn_view.py

from flask import jsonify, request
from models.txn import Txn, db


# 添加交易记录
def add_txn():
    data = request.get_json()
    new_txn = Txn(
        txnId=data['txnId'],
        txnDateTime=data['txnDateTime'],
        txnType=data['txnType'],
        txnCpty=data['txnCpty'],
        prodDesc=data['prodDesc'],
        incOrExp=data['incOrExp'],
        txnAmount=data['txnAmount'],
        payMethod=data['payMethod'],
        txnStatus=data['txnStatus']
    )
    db.session.add(new_txn)
    db.session.commit()
    return jsonify({'message': 'Transaction added successfully'})


# 删除交易记录
def delete_txn(txn_id):
    txn = Txn.query.get(txn_id)
    if not txn:
        return jsonify({'error': 'Transaction not found'})
    db.session.delete(txn)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted successfully'})


# 修改交易记录
def update_txn(txn_id):
    txn = Txn.query.get(txn_id)
    if not txn:
        return jsonify({'error': 'Transaction not found'})

    data = request.get_json()
    txn.txnId = data.get('txnId', txn.txnId)
    txn.txnDateTime = data.get('txnDateTime', txn.txnDateTime)
    txn.txnType = data.get('txnType', txn.txnType)
    txn.txnCpty = data.get('txnCpty', txn.txnCpty)
    txn.prodDesc = data.get('prodDesc', txn.prodDesc)
    txn.incOrExp = data.get('incOrExp', txn.incOrExp)
    txn.txnAmount = data.get('txnAmount', txn.txnAmount)
    txn.payMethod = data.get('payMethod', txn.payMethod)
    txn.txnStatus = data.get('txnStatus', txn.txnStatus)

    db.session.commit()
    return jsonify({'message': 'Transaction updated successfully'})


# 获取所有交易记录
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
            'txnStatus': txn.txnStatus
        })
    return jsonify(result)
