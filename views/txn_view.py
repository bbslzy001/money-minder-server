# money-minder-server\views\txn_view.py

from flask import request, jsonify
from services import txn_service


def add_txn():
    data = request.get_json()
    result = txn_service.add_txn(data)
    return jsonify(result)


def delete_txn(txn_id):
    result = txn_service.delete_txn(txn_id)
    return jsonify(result)


def update_txn(txn_id):
    data = request.get_json()
    result = txn_service.update_txn(txn_id, data)
    return jsonify(result)


def get_txns():
    result = txn_service.get_txns()
    return jsonify(result)
