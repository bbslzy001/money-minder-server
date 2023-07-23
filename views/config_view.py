# money-minder-server\views\config_view.py

from flask import jsonify, request

from services import config_service


def add_config():
    data = request.get_json()
    result = config_service.add_config(data)
    return jsonify(result)


def delete_config(config_id):
    result = config_service.delete_config(config_id)
    return jsonify(result)


def update_config(config_id):
    data = request.get_json()
    result = config_service.update_config(config_id, data)
    return jsonify(result)


def get_config(config_id):
    result = config_service.get_config(config_id)
    return jsonify(result)


def get_configs():
    result = config_service.get_configs()
    return jsonify(result)
