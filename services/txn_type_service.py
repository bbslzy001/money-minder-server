# money-minder-server\services\txn_type_service.py

from models import db
from models.txn_type import TxnType


# 提供增删改查方法
def add_txn_type(data):
    new_txn_type = TxnType(
        txn_type_name=data['txnTypeName']
    )
    db.session.add(new_txn_type)
    db.session.commit()
    txn_type_id = new_txn_type.txn_type_id  # 获取自增ID
    return {'message': 'TxnType added successfully', 'id': txn_type_id}


def delete_txn_type(txn_type_id):
    txn_type = TxnType.query.get(txn_type_id)
    if not txn_type:
        return {'error': 'TxnType not found'}
    db.session.delete(txn_type)
    db.session.commit()
    return {'message': 'TxnType deleted successfully'}


def update_txn_type(txn_type_id, data):
    txn_type = TxnType.query.get(txn_type_id)
    if not txn_type:
        return {'error': 'TxnType not found'}
    txn_type.txn_type_name = data.get('txnTypeName', txn_type.txn_type_name)
    db.session.commit()
    return {'message': 'TxnType updated successfully'}


def get_txn_types():
    txn_types = TxnType.query.all()
    result = []
    for txn_type in txn_types:
        result.append({
            'txnTypeId': txn_type.txn_type_id,
            'txnTypeName': txn_type.txn_type_name
        })
    return {'message': 'TxnType gotten successfully', 'result': result}
