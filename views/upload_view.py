# money-minder-server\views\upload_view.py

import os
from flask import request, jsonify
from werkzeug import utils
from services import txn_service, bill_service

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
# ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def receive_alipay_bill():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = utils.secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # 解析支付宝账单的逻辑
        return jsonify({'message': 'Alipay bill parsed successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400


def receive_wechat_bill():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = utils.secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # 解析微信账单的逻辑
        return jsonify({'message': 'WeChat bill parsed successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400


def _parse_alipay_bill():
    pass


def _parse_wechat_bill():
    pass
