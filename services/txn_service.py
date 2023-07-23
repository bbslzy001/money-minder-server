# money-minder-server\services\txn_service.py

from sqlalchemy import and_, update

from models import db
from models.txn import Txn


def add_txn(data):
    new_txn = Txn(
        txn_date_time=data['txnDateTime'],
        txn_cpty=data['txnCpty'],
        prod_desc=data['prodDesc'],
        inc_or_exp=data['incOrExp'],
        txn_amount=data['txnAmount'],
        pay_method=data['payMethod'],
        txn_status=data['txnStatus'],
        origin_txn_type=data['originTxnType'],
        txn_type_id=data['txnTypeId'],
        rule_id=data['ruleId'],
        bill_id=data['billId'],
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
    txn.txn_cpty = data.get('txnCpty', txn.txn_cpty)
    txn.prod_desc = data.get('prodDesc', txn.prod_desc)
    txn.inc_or_exp = data.get('incOrExp', txn.inc_or_exp)
    txn.txn_amount = data.get('txnAmount', txn.txn_amount)
    txn.pay_method = data.get('payMethod', txn.pay_method)
    txn.txn_status = data.get('txnStatus', txn.txn_status)
    # txn.origin_txn_type = data.get('originTxnType', txn.origin_txn_type)  # 不允许修改originTxnType
    txn.txn_type_id = data.get('txnTypeId', txn.txn_type_id)
    # txn.rule_id = data.get('ruleId', txn.rule_id)  # 不允许修改ruleId
    # txn.bill_id = data.get('billId', txn.bill_id)  # 不允许修改billId
    db.session.commit()
    return {'message': 'Transaction updated successfully'}


# 对应rule_view中的添加操作，将新规则应用于txns
def update_txns_by_added_rule(rule_id, rule):
    filters = []
    if rule['originTxnType'] != '/':
        filters.append(Txn.origin_txn_type == rule['originTxnType'])
    if rule['txnCpty'] != '/':
        filters.append(Txn.txn_cpty == rule['txnCpty'])
    if rule['prodDesc'] != '/':
        filters.append(Txn.prod_desc == rule['prodDesc'])

    stmt = update(Txn).where(and_(*filters)).values(rule_id=rule_id, txn_type_id=rule['txnTypeId'])
    db.session.execute(stmt)
    db.session.commit()

    return {'message': 'Transactions updated successfully by added rule'}


# 对应rule_view的删除操作，将对应txns的ruleId和txnTypeId置1
def update_txns_by_deleted_rule(rule_id):
    filters = [Txn.rule_id == rule_id]

    stmt = update(Txn).where(and_(*filters)).values(rule_id=1, txn_type_id=1)
    db.session.execute(stmt)
    db.session.commit()

    return {'message': 'Transactions updated successfully by removed rule'}


# 对应rule_view的修改操作，将对应txns的ruleId和txnTypeId置1，再将新规则应用于txns
def update_txns_by_updated_rule(rule_id, origin_rule, new_rule):
    # 除txnTypeId外，其他字段都相同
    if origin_rule['originTxnType'] == new_rule['originTxnType'] and \
            origin_rule['txnCpty'] == new_rule['txnCpty'] and \
            origin_rule['prodDesc'] == new_rule['prodDesc']:
        if origin_rule['txnTypeId'] != new_rule['txnTypeId']:
            filters = [Txn.rule_id == rule_id]

            stmt = update(Txn).where(and_(*filters)).values(txn_type_id=new_rule['txnTypeId'])
            db.session.execute(stmt)
            db.session.commit()
    # 除txnTypeId外，其他字段有变化
    else:
        # 先将原规则对应的txns的ruleId和txnTypeId置1
        filters = [Txn.rule_id == rule_id]

        stmt = update(Txn).where(and_(*filters)).values(rule_id=1, txn_type_id=1)
        db.session.execute(stmt)
        db.session.commit()

        # 再将新规则应用于txns
        filters = []
        if new_rule['originTxnType'] != '/':
            filters.append(Txn.origin_txn_type == new_rule['originTxnType'])
        if new_rule['txnCpty'] != '/':
            filters.append(Txn.txn_cpty == new_rule['txnCpty'])
        if new_rule['prodDesc'] != '/':
            filters.append(Txn.prod_desc == new_rule['prodDesc'])

        stmt = update(Txn).where(and_(*filters)).values(rule_id=rule_id, txn_type_id=new_rule['txnTypeId'])
        db.session.execute(stmt)
        db.session.commit()

    return {'message': 'Transactions updated successfully by updated rule'}


def get_txns():
    txns = Txn.query.all()
    result = []
    for txn in txns:
        result.append({
            'txnId': txn.txn_id,
            'txnDateTime': txn.txn_date_time,
            'txnCpty': txn.txn_cpty,
            'prodDesc': txn.prod_desc,
            'incOrExp': txn.inc_or_exp,
            'txnAmount': txn.txn_amount,
            'payMethod': txn.pay_method,
            'txnStatus': txn.txn_status,
            'originTxnType': txn.origin_txn_type,
            'txnTypeId': txn.txn_type_id,
            # 'ruleId': txn.rule_id,  # 不返回ruleId
            # 'billId': txn.bill_id,  # 不返回billId
        })
    return {'message': 'Transaction gotten successfully', 'result': result}
