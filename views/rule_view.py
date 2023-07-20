# money-minder-server\views\rule_view.py

from flask import request, jsonify

from services import rule_service


def add_rule():
    data = request.get_json()
    result = rule_service.add_rule(data)
    return jsonify(result)


def delete_rule(rule_id):
    result = rule_service.delete_rule(rule_id)
    return jsonify(result)


def update_rule(rule_id):
    data = request.get_json()
    result = rule_service.update_rule(rule_id, data)
    return jsonify(result)


def get_rules():
    result = rule_service.get_rules()
    return jsonify(result)
