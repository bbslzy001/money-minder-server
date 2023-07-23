# money-minder-server\views\txn_type_view.py

from flask import jsonify, request

from services import txn_type_service


def add_txn_type():
    data = request.get_json()
    result = txn_type_service.add_txn_type(data)
    return jsonify(result)


def delete_txn_type(txn_type_id):
    result = txn_type_service.delete_txn_type(txn_type_id)
    return jsonify(result)


def update_txn_type(txn_type_id):
    data = request.get_json()
    result = txn_type_service.update_txn_type(txn_type_id, data)
    return jsonify(result)


def get_txn_types():
    result = txn_type_service.get_txn_types()
    return jsonify(result)
