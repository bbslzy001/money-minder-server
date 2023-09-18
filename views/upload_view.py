# money-minder-server\views\upload_view.py

import os
import chardet
import csv
import numpy as np
import pandas as pd

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
        if bill_type == 'alipay':
            bill_id = _add_alipay_bill(filename, csvfile)
            if bill_id == 0:
                return False
            return _add_alipay_txn(bill_id, csvfile)
        elif bill_type == 'wechat':
            bill_id = _add_wechat_bill(filename, csvfile)
            if bill_id == 0:
                return False
            return _add_wechat_txn(bill_id, csvfile)


def _add_alipay_bill(filename, csvfile):
    result = None
    try:
        """
        csv_reader对象会影响到原始的csvfile对象
        使用csv.reader对象进行迭代时，它会调用csvfile的next()方法来获取下一行数据。
        由于Python中的文件对象并不能像列表或字典那样简单地复制，因此你无法创建csvfile对象的真正拷贝。
        """
        csv_reader = csv.reader(csvfile)

        bill_date = None
        for i, row in enumerate(csv_reader):
            if i == 4:
                bill_date = row[0]
                break

        csvfile.seek(0)  # 恢复到初始位置

        start_date = datetime.strptime(bill_date[bill_date.index('[') + 1: bill_date.index(']')], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(bill_date[bill_date.rindex('[') + 1: bill_date.rindex(']')], '%Y-%m-%d %H:%M:%S')

        bill_data = {
            'billName': filename,
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'billType': 'alipay',
        }

        result = bill_service.add_bill(bill_data)

        return result['id']
    except Exception as e:
        print(e)
        if result:
            bill_service.delete_bill(result['id'])  # 失败时自动删除该账单及所有已添加的交易记录
        return 0


def _add_alipay_txn(bill_id, csvfile):
    try:
        # 查询匹配规则和交易类型
        rules = rule_service.get_rules()['result']
        txn_types = txn_type_service.get_txn_types()['result']

        # 读取CSV文件(跳过前24行说明信息，忽略空行)
        df = pd.read_csv(csvfile, skiprows=24, skip_blank_lines=True)

        # 忽略最后一列（空列）
        df = df.iloc[:, :-1]

        # 删除指定列末尾的'\t'
        for column_name in ['交易订单号', '商家订单号']:
            df[column_name] = df[column_name].str.rstrip('\t')

        # 将NaN值替换为'/'
        df.fillna('/', inplace=True)

        # 将"不计收支"替换为"不计"
        df['收/支'] = df['收/支'].replace('不计收支', '不计')

        # 格式化“交易时间”列
        # df['交易时间'] = pd.to_datetime(df['交易时间'])

        # 添加“规则ID”和“交易类型ID”，默认“未应用规则”、“交易类型为其他”
        df = df.assign(规则ID=None, 交易类型ID=1)

        for index, row in df.iterrows():
            rule = next((r for r in rules
                         if (r['originTxnType'] == '/' or row['交易分类'] == r['originTxnType']) and
                         (r['txnCpty'] == '/' or row['交易对方'] == r['txnCpty']) and
                         (r['prodDesc'] == '/' or row['商品说明'] == r['prodDesc'])), None)
            # 找到匹配的规则
            if rule is not None:
                df.at[index, '规则ID'] = rule['ruleId']
                df.at[index, '交易类型ID'] = rule['txnTypeId']
            # 没有应用任何规则，判断其交易类型是否已存在于数据库中
            else:
                txn_type = next((t for t in txn_types if t['txnTypeName'] == row['交易分类']), None)
                # 找到匹配的交易类型
                if txn_type is not None:
                    df.at[index, '交易类型ID'] = txn_type['txnTypeId']

        # 按商家订单号进行分组，筛选出存在退款的交易记录，组内按交易时间倒序排列
        grouped = df.groupby('商家订单号').filter(lambda x: len(x) > 1)
        grouped = grouped.sort_values(by=['商家订单号', '交易时间'], ascending=[True, False])

        # 格式化“收/支”列
        grouped['收/支'] = '不计'

        # 格式化“交易状态”列
        grouped_last = grouped.groupby('商家订单号').last()
        mask = grouped['交易订单号'].isin(grouped_last['交易订单号'])
        grouped.loc[mask, '交易状态'] = '交易关闭'

        # 格式化“交易分类”、“规则ID”、“交易类型ID”列
        grouped['交易分类'] = grouped['商家订单号'].map(grouped_last['交易分类'])
        grouped['规则ID'] = grouped['商家订单号'].map(grouped_last['规则ID'])
        grouped['交易类型ID'] = grouped['商家订单号'].map(grouped_last['交易类型ID'])

        # 将处理后的数据覆盖到原数据集中
        mask = df['交易订单号'].isin(grouped['交易订单号'])
        df.loc[mask, '交易分类'] = grouped['交易分类'].values
        df.loc[mask, '收/支'] = grouped['收/支'].values
        df.loc[mask, '交易状态'] = grouped['交易状态'].values

        # 将DataFrame逐行插入数据库
        for index, row in df.iterrows():
            txn_data = {
                'txnDateTime': row['交易时间'],
                'txnCpty': row['交易对方'],
                'prodDesc': row['商品说明'],
                'incOrExp': row['收/支'],
                'txnAmount': row['金额'],
                'payMethod': row['收/付款方式'],
                'txnStatus': row['交易状态'],
                'originTxnType': row['交易分类'],
                'txnTypeId': row['交易类型ID'],
                'ruleId': row['规则ID'],
                'billId': bill_id,
            }
            txn_service.add_txn(txn_data)

        return True
    except Exception as e:
        print(e)
        bill_service.delete_bill(bill_id)
        return False


def _add_wechat_bill(filename, csvfile):
    result = None
    try:
        csv_reader = csv.reader(csvfile)

        bill_date = None
        for i, row in enumerate(csv_reader):
            if i == 2:
                bill_date = row[0]
                break

        csvfile.seek(0)  # 恢复到初始位置

        start_date = datetime.strptime(bill_date[bill_date.index('[') + 1: bill_date.index(']')], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(bill_date[bill_date.rindex('[') + 1: bill_date.rindex(']')], '%Y-%m-%d %H:%M:%S')

        bill_data = {
            'billName': filename,
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'billType': 'wechat',
        }

        result = bill_service.add_bill(bill_data)

        return result['id']
    except Exception as e:
        print(e)
        if result:
            bill_service.delete_bill(result['id'])  # 失败时自动删除该账单及所有已添加的交易记录
        return 0


def _add_wechat_txn(bill_id, csvfile):
    try:
        # 查询匹配规则和交易类型
        rules = rule_service.get_rules()['result']
        txn_types = txn_type_service.get_txn_types()['result']

        # 读取CSV文件(跳过前16行说明信息，忽略空行)
        df = pd.read_csv(csvfile, skiprows=16, skip_blank_lines=True)

        # 格式化“交易单号”、“商户单号”列
        for column_name in ['交易单号', '商户单号']:
            df[column_name] = df[column_name].str.rstrip('\t')

        # 格式化“金额(元)”列
        df['金额(元)'] = df['金额(元)'].str.lstrip('¥')

        # 将"不计收支"替换为"不计"
        df['收/支'] = df['收/支'].replace('不计收支', '不计')

        # 格式化“交易时间”列
        # df['交易时间'] = pd.to_datetime(df['交易时间'])

        # 添加“规则ID”和“交易类型ID”，默认“未应用规则”、“交易类型为其他”
        df = df.assign(规则ID=None, 交易类型ID=1)

        for index, row in df.iterrows():
            rule = next((r for r in rules
                         if (r['originTxnType'] == '/' or row['交易类型'] == r['originTxnType']) and
                         (r['txnCpty'] == '/' or row['交易对方'] == r['txnCpty']) and
                         (r['prodDesc'] == '/' or row['商品'] == r['prodDesc'])), None)
            # 找到匹配的规则
            if rule is not None:
                df.at[index, '规则ID'] = rule['ruleId']
                df.at[index, '交易类型ID'] = rule['txnTypeId']
            # 没有应用任何规则，判断其交易类型是否已存在于数据库中
            else:
                txn_type = next((t for t in txn_types if t['txnTypeName'] == row['交易类型']), None)
                # 找到匹配的交易类型
                if txn_type is not None:
                    df.at[index, '交易类型ID'] = txn_type['txnTypeId']

        conditions = [
            df['当前状态'].isin(['对方已收钱', '已存入零钱', '已到账', '已转账', '支付成功']),
            (df['当前状态'].isin(['对方已退还', '已全额退款'])) & (df['收/支'] == '收入'),
            (df['当前状态'].isin(['对方已退还', '已全额退款'])) & (df['收/支'] == '支出'),
        ]

        choices = ['交易成功', '退款成功', '交易关闭']

        df['当前状态'] = np.select(conditions, choices, default=df['当前状态'])

        mask = df['当前状态'].isin(['对方已退还', '已全额退款'])
        df.loc[mask, '收/支'] = '不计'

        # 将DataFrame逐行插入数据库
        for index, row in df.iterrows():
            txn_data = {
                'txnDateTime': row['交易时间'],
                'txnCpty': row['交易对方'],
                'prodDesc': row['商品'],
                'incOrExp': row['收/支'],
                'txnAmount': row['金额(元)'],
                'payMethod': row['支付方式'],
                'txnStatus': row['当前状态'],
                'originTxnType': row['交易类型'],
                'txnTypeId': row['交易类型ID'],
                'ruleId': row['规则ID'],
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
