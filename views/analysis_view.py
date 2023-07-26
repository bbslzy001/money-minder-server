# money-minder-server\views\analysis_view.py

from flask import jsonify, request

from services import txn_service


def get_count():
    data = request.get_json()
    result = txn_service.get_count(data['startDate'], data['endDate'])
    return jsonify(result)


def get_amount():
    data = request.get_json()
    result = txn_service.get_amount(data['startDate'], data['endDate'], data['incOrExp'])
    return jsonify(result)


def get_txns_by_amount_rank():
    data = request.get_json()
    result = txn_service.get_txns_by_amount_rank(data['startDate'], data['endDate'], data['incOrExp'])
    return jsonify(result)


def get_amount_by_type():
    data = request.get_json()
    result = txn_service.get_amount_by_type(data['startDate'], data['endDate'], data['incOrExp'])
    return jsonify(result)


def get_count_by_time():
    data = request.get_json()
    result = txn_service.get_count_by_time(data['startDate'], data['endDate'], data['incOrExp'])
    return jsonify(result)
