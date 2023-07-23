# money-minder-server\services\config_service.py

from models import db
from models.config import Config


def add_config(data):
    new_config = Config(
        config_name=data['configName'],
        config_value=data['configValue'],
    )
    db.session.add(new_config)
    db.session.commit()
    config_id = new_config.config_id  # 获取自增ID
    return {'message': 'Config added successfully', 'id': config_id}


def delete_config(config_id):
    config = Config.query.get(config_id)
    if not config:
        return {'error': 'Config not found'}
    db.session.delete(config)
    db.session.commit()
    return {'message': 'Config deleted successfully'}


def update_config(config_id, data):
    config = Config.query.get(config_id)
    if not config:
        return {'error': 'Config not found'}
    # config.config_name = data.get('configName', config.config_name)  # 不允许修改configName
    config.config_value = data.get('configValue', config.config_value)
    db.session.commit()
    return {'message': 'Config updated successfully'}


def get_config(config_id):
    config = Config.query.get(config_id)
    if not config:
        return {'error': 'Config not found'}
    result = {
        'configId': config.config_id,
        'configName': config.config_name,
        'configValue': config.config_value,
    }
    return {'message': 'Config gotten successfully', 'result': result}


def get_configs():
    configs = Config.query.all()
    result = []
    for config in configs:
        result.append({
            'configId': config.config_id,
            'configName': config.config_name,
            'configValue': config.config_value,
        })
    return {'message': 'Config gotten successfully', 'result': result}
