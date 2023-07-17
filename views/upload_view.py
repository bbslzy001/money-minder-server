# money-minder-server\views\upload_view.py

import os
import chardet
import csv

from datetime import datetime
from flask import request, jsonify
from werkzeug.utils import secure_filename

from services import txn_service, bill_service

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}


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
        if 'id' in result:
            bill_id = result['id']
            success = _parse_alipay_bill(filename, bill_id)
            if success:
                return jsonify({'message': 'Alipay bill parsed successfully'}), 200
            else:
                bill_service.delete_bill(bill_id)  # 失败时自动删除该账单及所有已添加的交易记录
                # os.remove(os.path.join(UPLOAD_FOLDER, filename))  # 删除上传的账单文件
                return jsonify({'error': 'Failed to parse Alipay bill'}), 500
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
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # 自动检测文件编码
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
            encoding = result['encoding']
            confidence = result['confidence']
            if confidence < 0.95:
                encoding = 'utf-8'  # 使用默认编码（如utf-8）解析文件

        with open(file_path, 'r', encoding=encoding, errors='ignore') as csvfile:
            csv_reader = csv.reader(csvfile)

            # 跳过前24行
            for _ in range(24):
                next(csv_reader)

            # 处理第25行，获取所需字段的列索引
            header = next(csv_reader)
            print(header)
            col_indices = {
                'txnDateTime': header.index('交易时间'),
                'txnType': header.index('交易分类'),
                'txnCpty': header.index('交易对方'),
                'prodDesc': header.index('商品说明'),
                'incOrExp': header.index('收/支'),
                'txnAmount': header.index('金额'),
                'payMethod': header.index('收/付款方式'),
                'txnStatus': header.index('交易状态'),
                'txnNumber': header.index('商家订单号')
            }

            # 用于记录 incOrExp 为 "不计收支" 的 txnNumber
            txn_numbers = {}

            # 根据所需字段的列索引提取数据并插入Txn表
            for line in csv_reader:
                raw_txn_datetime = line[col_indices['txnDateTime']]
                txn_type = line[col_indices['txnType']]
                inc_or_exp = line[col_indices['incOrExp']]
                txn_status = line[col_indices['txnStatus']]
                pay_method = line[col_indices['payMethod']]
                txn_number = line[col_indices['txnNumber']].strip()  # 去除 txn_number 两侧的空格

                # 将 txnDateTime 转换为 datetime 对象
                parsed_txn_datetime = datetime.strptime(raw_txn_datetime, '%Y-%m-%d %H:%M:%S')
                formatted_txn_datetime = parsed_txn_datetime.strftime('%Y-%m-%d %H:%M:%S')

                # 根据条件更新 txn_type 的值
                if txn_type == '退款':
                    txn_type = '其他'

                # 根据条件更新 inc_or_exp 和 txn_status 的值
                if txn_number in txn_numbers:
                    if inc_or_exp != '不计收支':
                        del txn_numbers[txn_number]
                    inc_or_exp = '不计'
                    if txn_status == '交易成功':
                        txn_status = '交易关闭'
                elif inc_or_exp == "不计收支":
                    inc_or_exp = "不计"
                    txn_numbers[txn_number] = True

                # 根据条件更新 pay_method 的值
                if pay_method == "":
                    pay_method = "/"

                txn_data = {
                    'txnDateTime': formatted_txn_datetime,
                    'txnType': txn_type,
                    'txnCpty': line[col_indices['txnCpty']],
                    'prodDesc': line[col_indices['prodDesc']],
                    'incOrExp': inc_or_exp,
                    'txnAmount': line[col_indices['txnAmount']],
                    'payMethod': pay_method,
                    'txnStatus': txn_status,
                    'billId': bill_id
                }
                txn_service.add_txn(txn_data)
        return True
    except Exception as e:
        print(e)
        return False


def _parse_wechat_bill():
    pass
