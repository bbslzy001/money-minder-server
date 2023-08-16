# money-minder-server\views\analysis_view.py

from flask import jsonify, request

from services import txn_service


def get_count(date_range_count):
    data = request.get_json()
    if date_range_count == 1:
        result = txn_service.get_count(data['startDate'], data['endDate'])
        return jsonify(result)
    elif date_range_count == 2:
        result1 = txn_service.get_count(data['startDate'][0], data['endDate'][0])
        result2 = txn_service.get_count(data['startDate'][1], data['endDate'][1])
        result = {
            'txnCount': {
                'lastValue': result1['result']['txnCount'],
                'currentValue': result2['result']['txnCount'],
            },
        }
        return jsonify({'result': result})
    return jsonify({'error': 'Invalid date range count'})


def get_amount(date_range_count):
    data = request.get_json()
    if date_range_count == 1:
        result = txn_service.get_amount(data['startDate'], data['endDate'], data['incOrExp'])
        return jsonify(result)
    elif date_range_count == 2:
        result1 = txn_service.get_amount(data['startDate'][0], data['endDate'][0], data['incOrExp'])
        result2 = txn_service.get_amount(data['startDate'][1], data['endDate'][1], data['incOrExp'])
        result = {
            'txnAmount': {
                'lastValue': result1['result']['txnAmount'],
                'currentValue': result2['result']['txnAmount'],
            },
        }
        return jsonify({'result': result})
    return jsonify({'error': 'Invalid date range count'})


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


def get_amount_by_date():
    data = request.get_json()
    result = txn_service.get_amount_by_date(data['startDate'], data['endDate'], data['incOrExp'])
    return jsonify(result)
