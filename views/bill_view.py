# money-minder-server\views\bill_view.py

from flask import jsonify, request

from services import bill_service


def add_bill():
    data = request.get_json()
    result = bill_service.add_bill(data)
    return jsonify(result)


def delete_bill(bill_id):
    result = bill_service.delete_bill(bill_id)
    return jsonify(result)


def update_bill(bill_id):
    data = request.get_json()
    result = bill_service.update_bill(bill_id, data)
    return jsonify(result)


def get_bills():
    result = bill_service.get_bills()
    return jsonify(result)
