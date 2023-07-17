# money-minder-server\views\__init__.py

from flask import Blueprint
from views import txn_view, upload_view


api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api_blueprint.route('/txn', methods=['POST'])(txn_view.add_txn)
api_blueprint.route('/txn/<int:txn_id>', methods=['DELETE'])(txn_view.delete_txn)
api_blueprint.route('/txn/<int:txn_id>', methods=['PUT'])(txn_view.update_txn)
api_blueprint.route('/txn', methods=['GET'])(txn_view.get_txns)

api_blueprint.route('/upload/alipay', methods=['POST'])(upload_view.receive_alipay_bill)
api_blueprint.route('/upload/wechat', methods=['POST'])(upload_view.receive_wechat_bill)
