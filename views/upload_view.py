# money-minder-server\views\upload_view.py

import os
import csv

from flask import request, jsonify
from werkzeug.utils import secure_filename

from services import txn_service, bill_service


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
# ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def receive_alipay_bill():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and _allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        result = bill_service.add_bill({'billName': filename})
        if 'billId' in result:
            bill_id = result['billId']
            _parse_alipay_bill(filename, bill_id)
            return jsonify({'message': 'Alipay bill parsed successfully'}), 200
        else:
            return jsonify({'error': 'Failed to add bill'}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400


def receive_wechat_bill():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and _allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # 解析微信账单的逻辑
        return jsonify({'message': 'WeChat bill parsed successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400


def _parse_alipay_bill(filename, bill_id):
    with open(os.path.join(UPLOAD_FOLDER, filename), 'r', encoding='utf-8-sig') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            txn_data = {
                'txnDateTime': row['交易时间'],
                'txnType': row['交易分类'],
                'txnCpty': row['交易对方'],
                'prodDesc': row['商品说明'],
                'incOrExp': row['收/支'],
                'txnAmount': row['金额'],
                'payMethod': row['收/付款方式'],
                'txnStatus': row['交易状态'],
                'billId': bill_id
            }
            txn_service.add_txn(txn_data)


def _parse_wechat_bill():
    pass
