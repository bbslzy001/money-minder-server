# money-minder-server\views\upload_view.py

import os
import chardet
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
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # 自动检测文件编码
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    encoding = result['encoding']

    with open(file_path, 'r', encoding=encoding) as csvfile:
        csv_reader = csv.reader(csvfile)

        # 跳过前24行
        for _ in range(24):
            next(csv_reader)

        # 处理第25行，获取所需字段的列索引
        header = next(csv_reader)
        col_indices = {
            'txnDateTime': header.index('交易时间'),
            'txnType': header.index('交易分类'),
            'txnCpty': header.index('交易对方'),
            'prodDesc': header.index('商品说明'),
            'incOrExp': header.index('收/支'),
            'txnAmount': header.index('金额'),
            'payMethod': header.index('收/付款方式'),
            'txnStatus': header.index('交易状态')
        }

        # 根据所需字段的列索引提取数据并插入Txn表
        for line in csv_reader:
            txn_data = {
                'txnDateTime': line[col_indices['txnDateTime']],
                'txnType': line[col_indices['txnType']],
                'txnCpty': line[col_indices['txnCpty']],
                'prodDesc': line[col_indices['prodDesc']],
                'incOrExp': line[col_indices['incOrExp']],
                'txnAmount': line[col_indices['txnAmount']],
                'payMethod': line[col_indices['payMethod']],
                'txnStatus': line[col_indices['txnStatus']],
                'billId': bill_id
            }
            txn_service.add_txn(txn_data)


def _parse_wechat_bill():
    pass
