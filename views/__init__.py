# money-minder-server\views\__init__.py

from flask import Blueprint

from views import bill_view, config_view, rule_view, txn_type_view, txn_view, upload_view


api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api_blueprint.route('/txn/delete/<int:txn_id>', methods=['DELETE'])(txn_view.delete_txn)
api_blueprint.route('/txn/update/<int:txn_id>', methods=['PUT'])(txn_view.update_txn)
api_blueprint.route('/txn/getall', methods=['GET'])(txn_view.get_txns)

api_blueprint.route('/bill/delete/<int:bill_id>', methods=['DELETE'])(bill_view.delete_bill)
api_blueprint.route('/bill/update/<int:bill_id>', methods=['PUT'])(bill_view.update_bill)
api_blueprint.route('/bill/getall', methods=['GET'])(bill_view.get_bills)

api_blueprint.route('/upload/<string:bill_type>', methods=['POST'])(upload_view.receive_bill)

api_blueprint.route('/txn-type/add', methods=['POST'])(txn_type_view.add_txn_type)
api_blueprint.route('/txn-type/delete/<int:txn_type_id>', methods=['DELETE'])(txn_type_view.delete_txn_type)
api_blueprint.route('/txn-type/update/<int:txn_type_id>', methods=['PUT'])(txn_type_view.update_txn_type)
api_blueprint.route('/txn-type/getall', methods=['GET'])(txn_type_view.get_txn_types)

api_blueprint.route('/rule/add', methods=['POST'])(rule_view.add_rule)
api_blueprint.route('/rule/delete/<int:rule_id>', methods=['DELETE'])(rule_view.delete_rule)
api_blueprint.route('/rule/update/<int:rule_id>', methods=['PUT'])(rule_view.update_rule)
api_blueprint.route('/rule/getall', methods=['GET'])(rule_view.get_rules)

api_blueprint.route('/rule/add/apply-txns', methods=['POST'])(rule_view.add_rule_apply_txns)
api_blueprint.route('/rule/delete/apply-txns/<int:rule_id>', methods=['DELETE'])(rule_view.delete_rule_apply_txns)
api_blueprint.route('/rule/update/apply-txns/<int:rule_id>', methods=['PUT'])(rule_view.update_rule_apply_txns)

api_blueprint.route('/config/update/<int:config_id>', methods=['PUT'])(config_view.update_config)
api_blueprint.route('/config/get/<int:config_id>', methods=['GET'])(config_view.get_config)
