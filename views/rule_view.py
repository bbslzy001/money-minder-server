# money-minder-server\views\rule_view.py

from flask import jsonify, request

from services import rule_service, txn_service


def add_rule():
    data = request.get_json()
    result = rule_service.add_rule(data)
    return jsonify(result)


def add_rule_apply_txns():
    data = request.get_json()
    result1 = rule_service.add_rule(data)
    result2 = txn_service.update_txns_by_added_rule(result1['id'], data)
    return jsonify(result2)


def delete_rule(rule_id):
    result = rule_service.delete_rule(rule_id)
    return jsonify(result)


def delete_rule_apply_txns(rule_id):
    rule_service.delete_rule(rule_id)
    result = txn_service.update_txns_by_deleted_rule(rule_id)
    return jsonify(result)


def update_rule(rule_id):
    data = request.get_json()
    result = rule_service.update_rule(rule_id, data)
    return jsonify(result)


def update_rule_apply_txns(rule_id):
    data = request.get_json()
    original_rule = rule_service.get_rule(rule_id)
    rule_service.update_rule(rule_id, data)
    result = txn_service.update_txns_by_updated_rule(rule_id, original_rule, data)
    return jsonify(result)


def get_rules():
    result = rule_service.get_rules()
    return jsonify(result)
