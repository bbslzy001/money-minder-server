# money-minder-server\services\rule_service.py

from models import db
from models.rule import Rule


def add_rule(data):
    new_rule = Rule(
        origin_txn_type=data['originTxnType'],
        txn_cpty=data['txnCpty'],
        prod_desc=data['prodDesc'],
        txn_type_id=data['txnTypeId'],
    )
    db.session.add(new_rule)
    db.session.commit()
    rule_id = new_rule.rule_id  # 获取自增ID
    return {'message': 'Rule added successfully', 'id': rule_id}


def delete_rule(rule_id):
    rule = Rule.query.get(rule_id)
    if not rule:
        return {'error': 'Rule not found'}
    db.session.delete(rule)
    db.session.commit()
    return {'message': 'Rule deleted successfully'}


def update_rule(rule_id, data):
    rule = Rule.query.get(rule_id)
    if not rule:
        return {'error': 'Rule not found'}
    rule.origin_txn_type = data.get('originTxnType', rule.origin_txn_type)
    rule.txn_cpty = data.get('txnCpty', rule.txn_cpty)
    rule.prod_desc = data.get('prodDesc', rule.prod_desc)
    rule.txn_type_id = data.get('txnTypeId', rule.txn_type_id)
    db.session.commit()
    return {'message': 'Rule updated successfully'}


def get_rule(rule_id):
    rule = Rule.query.get(rule_id)
    if not rule:
        return {'error': 'Rule not found'}
    result = {
        'ruleId': rule.rule_id,
        'originTxnType': rule.origin_txn_type,
        'txnCpty': rule.txn_cpty,
        'prodDesc': rule.prod_desc,
        'txnTypeId': rule.txn_type_id,
    }
    return {'message': 'Rule gotten successfully', 'result': result}


def get_rules():
    rules = Rule.query.all()
    result = [{
        'ruleId': rule.rule_id,
        'originTxnType': rule.origin_txn_type,
        'txnCpty': rule.txn_cpty,
        'prodDesc': rule.prod_desc,
        'txnTypeId': rule.txn_type_id,
    } for rule in rules]
    return {'message': 'Rule gotten successfully', 'result': result}
