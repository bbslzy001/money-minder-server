# money-minder-server\views\init.py

from flask import Blueprint
from views.txn_view import add_txn, delete_txn, update_txn, get_txns
from views.upload_view import parse_alipay_bill, parse_wechat_bill


api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api_blueprint.route('/txn', methods=['POST'])(add_txn)
api_blueprint.route('/txn/<int:txn_id>', methods=['DELETE'])(delete_txn)
api_blueprint.route('/txn/<int:txn_id>', methods=['PUT'])(update_txn)
api_blueprint.route('/txn', methods=['GET'])(get_txns)

api_blueprint.route('/upload/alipay', methods=['POST'])(parse_alipay_bill)
api_blueprint.route('/upload/wechat', methods=['POST'])(parse_wechat_bill)
