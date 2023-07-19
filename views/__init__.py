# money-minder-server\views\__init__.py

from flask import Blueprint

from views import txn_view, bill_view, upload_view


api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api_blueprint.route('/txn/delete/<int:txn_id>', methods=['DELETE'])(txn_view.delete_txn)
api_blueprint.route('/txn/update/<int:txn_id>', methods=['PUT'])(txn_view.update_txn)
api_blueprint.route('/txn/getall', methods=['GET'])(txn_view.get_txns)

api_blueprint.route('/bill/delete/<int:bill_id>', methods=['DELETE'])(bill_view.delete_bill)
api_blueprint.route('/bill/update/<int:bill_id>', methods=['PUT'])(bill_view.update_bill)
api_blueprint.route('/bill/getall', methods=['GET'])(bill_view.get_bills)

api_blueprint.route('/upload/<string:bill_type>', methods=['POST'])(upload_view.receive_bill)
