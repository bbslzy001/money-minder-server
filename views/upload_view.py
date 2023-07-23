# money-minder-server\views\upload_view.py

import os
import chardet
import csv

from datetime import datetime
from flask import jsonify, request
from werkzeug.utils import secure_filename

from services import bill_service, rule_service, txn_type_service, txn_service

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def receive_bill(bill_type):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and _allowed_file(file.filename):
        filename = secure_filename(file.filename)  # 获取文件名称
        filepath = os.path.join(UPLOAD_FOLDER, filename)  # 获取文件路径
        file.save(filepath)  # 保存文件
        encoding = detect_encoding(filepath)  # 获取文件编码

        is_succeed = _parse_bill(filename, filepath, encoding, bill_type)  # 解析文件

        if is_succeed:
            return jsonify({'message': 'Bill parsed successfully'}), 200
        else:
            return jsonify({'error': 'Failed to parse bill'}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400


def _parse_bill(filename, filepath, encoding, bill_type):
    with open(filepath, 'r', encoding=encoding, errors='ignore') as csvfile:
        csv_reader = csv.reader(csvfile)

        if bill_type == 'alipay':
            bill_id = _add_alipay_bill(filename, csv_reader)
            if bill_id == 0:
                return False
            return _add_alipay_txn(bill_id, csv_reader)
        elif bill_type == 'wechat':
            bill_id = _add_wechat_bill(filename, csv_reader)
            if bill_id == 0:
                return False
            return _add_wechat_txn(bill_id, csv_reader)


def _add_alipay_bill(filename, csv_reader):
    result = None
    try:
        # 跳过前4行
        for _ in range(4):
            next(csv_reader)

        # 处理第5行，获取账单的起止日期
        bill_date = next(csv_reader)[0]
        start_date = datetime.strptime(bill_date[bill_date.index('[') + 1: bill_date.index(']')], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(bill_date[bill_date.rindex('[') + 1: bill_date.rindex(']')], '%Y-%m-%d %H:%M:%S')
        bill_data = {
            'billName': filename,
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'billType': 'alipay',
        }

        # 跳过第6-24行，共19行
        for _ in range(19):
            next(csv_reader)  # 引用传递

        result = bill_service.add_bill(bill_data)

        return result['id']
    except Exception as e:
        print(e)
        if result:
            bill_service.delete_bill(result['id'])  # 失败时自动删除该账单及所有已添加的交易记录
        return 0


def _add_alipay_txn(bill_id, csv_reader):
    try:
        # 处理第25行，获取所需字段的列索引
        header = next(csv_reader)
        col_indices = {
            'txnDateTime': header.index('交易时间'),
            'txnCpty': header.index('交易对方'),
            'prodDesc': header.index('商品说明'),
            'incOrExp': header.index('收/支'),
            'txnAmount': header.index('金额'),
            'payMethod': header.index('收/付款方式'),
            'txnStatus': header.index('交易状态'),
            'originTxnType': header.index('交易分类'),
            'txnNumber': header.index('商家订单号'),
        }

        # 用于记录 incOrExp 为 "不计收支" 的 txnNumber
        txn_numbers = {}

        # 查询匹配规则和交易类型
        rules = rule_service.get_rules()['result']
        txn_types = txn_type_service.get_txn_types()['result']

        # 根据所需字段的列索引提取数据并插入Txn表
        for line in csv_reader:
            txn_datetime = line[col_indices['txnDateTime']]
            txn_cpty = line[col_indices['txnCpty']]
            prod_desc = line[col_indices['prodDesc']]
            inc_or_exp = line[col_indices['incOrExp']]
            txn_amount = line[col_indices['txnAmount']]
            pay_method = line[col_indices['payMethod']]
            txn_status = line[col_indices['txnStatus']]
            origin_txn_type = line[col_indices['originTxnType']]
            txn_number = line[col_indices['txnNumber']].strip()  # 去除 txn_number 两侧的空格

            # 默认为其他且未应用规则
            txn_type_id = 1
            rule_id = None

            # 将 txnDateTime 转换为 datetime 对象
            parsed_txn_datetime = datetime.strptime(txn_datetime, '%Y-%m-%d %H:%M:%S')
            txn_datetime = parsed_txn_datetime.strftime('%Y-%m-%d %H:%M:%S')

            # 根据条件更新 txn_type 的值
            for rule in rules:
                if (rule['originTxnType'] == '/' or rule['originTxnType'] == origin_txn_type) and \
                        (rule['txnCpty'] == '/' or rule['txnCpty'] == txn_cpty) and \
                        (rule['prodDesc'] == '/' or rule['prodDesc'] == prod_desc):
                    txn_type_id = rule['txnTypeId']
                    rule_id = rule['ruleId']
                    break
            if rule_id is None:
                txn_type_id = next((t['txnTypeId'] for t in txn_types if t['txnTypeName'] == origin_txn_type), txn_type_id)

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
                'txnDateTime': txn_datetime,
                'txnCpty': txn_cpty,
                'prodDesc': prod_desc,
                'incOrExp': inc_or_exp,
                'txnAmount': txn_amount,
                'payMethod': pay_method,
                'txnStatus': txn_status,
                'originTxnType': origin_txn_type,
                'txnTypeId': txn_type_id,
                'ruleId': rule_id,
                'billId': bill_id,
            }

            txn_service.add_txn(txn_data)

        return True
    except Exception as e:
        print(e)
        bill_service.delete_bill(bill_id)
        return False


def _add_wechat_bill(filename, csv_reader):
    result = None
    try:
        # 跳过前2行
        for _ in range(2):
            next(csv_reader)

        # 处理第3行，获取账单的起止日期
        bill_date = next(csv_reader)[0]
        start_date = datetime.strptime(bill_date[bill_date.index('[') + 1: bill_date.index(']')], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(bill_date[bill_date.rindex('[') + 1: bill_date.rindex(']')], '%Y-%m-%d %H:%M:%S')
        bill_data = {
            'billName': filename,
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'billType': 'wechat',
        }

        # 跳过第4-16行，共13行
        for _ in range(13):
            next(csv_reader)  # 引用传递

        result = bill_service.add_bill(bill_data)

        return result['id']
    except Exception as e:
        print(e)
        if result:
            bill_service.delete_bill(result['id'])  # 失败时自动删除该账单及所有已添加的交易记录
        return 0


def _add_wechat_txn(bill_id, csv_reader):
    try:
        # 处理第17行，获取所需字段的列索引
        header = next(csv_reader)
        col_indices = {
            'txnDateTime': header.index('交易时间'),
            'txnCpty': header.index('交易对方'),
            'prodDesc': header.index('商品'),
            'incOrExp': header.index('收/支'),
            'txnAmount': header.index('金额(元)'),
            'payMethod': header.index('支付方式'),
            'txnStatus': header.index('当前状态'),
            'originTxnType': header.index('交易类型'),
        }

        # 查询匹配规则和交易类型
        rules = rule_service.get_rules()['result']
        txn_types = txn_type_service.get_txn_types()['result']

        # 根据所需字段的列索引提取数据并插入Txn表
        for line in csv_reader:
            txn_datetime = line[col_indices['txnDateTime']]
            txn_cpty = line[col_indices['txnCpty']]
            prod_desc = line[col_indices['prodDesc']]
            inc_or_exp = line[col_indices['incOrExp']]
            txn_amount = line[col_indices['txnAmount']]
            pay_method = line[col_indices['payMethod']]
            txn_status = line[col_indices['txnStatus']]
            origin_txn_type = line[col_indices['originTxnType']]

            # 默认为其他且未应用规则
            txn_type_id = 1
            rule_id = None

            # 将 txnDateTime 转换为 datetime 对象
            parsed_txn_datetime = datetime.strptime(txn_datetime, '%Y-%m-%d %H:%M:%S')
            txn_datetime = parsed_txn_datetime.strftime('%Y-%m-%d %H:%M:%S')

            # 根据条件更新 txn_type 的值
            for rule in rules:
                if (rule['originTxnType'] == '/' or rule['originTxnType'] == origin_txn_type) and \
                        (rule['txnCpty'] == '/' or rule['txnCpty'] == txn_cpty) and \
                        (rule['prodDesc'] == '/' or rule['prodDesc'] == prod_desc):
                    txn_type_id = rule['txnTypeId']
                    rule_id = rule['ruleId']
                    break
            if rule_id is None:
                txn_type_id = next((t['txnTypeId'] for t in txn_types if t['txnTypeName'] == origin_txn_type), txn_type_id)

            txn_amount = txn_amount[1:]

            if txn_status in ('对方已收钱', '已存入零钱', '已到账', '已转账', '支付成功'):
                txn_status = '交易成功'
            elif txn_status in ('对方已退还', '已全额退款'):
                if inc_or_exp == '收入':
                    txn_status = '退款成功'
                elif inc_or_exp == '支出':
                    txn_status = '交易关闭'
                inc_or_exp = '不计'

            txn_data = {
                'txnDateTime': txn_datetime,
                'txnCpty': txn_cpty,
                'prodDesc': prod_desc,
                'incOrExp': inc_or_exp,
                'txnAmount': txn_amount,
                'payMethod': pay_method,
                'txnStatus': txn_status,
                'originTxnType': origin_txn_type,
                'txnTypeId': txn_type_id,
                'ruleId': rule_id,
                'billId': bill_id,
            }

            txn_service.add_txn(txn_data)

        return True
    except Exception as e:
        print(e)
        bill_service.delete_bill(bill_id)
        return False


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        if result['confidence'] < 0.95:
            return 'utf-8'  # 使用默认编码（如utf-8）解析文件
        return result['encoding']
