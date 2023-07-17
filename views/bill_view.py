# money-minder-server\views\bill_view.py

from flask import jsonify, request
from models.bill import Bill, db


# 添加账单记录
def add_bill():
    data = request.get_json()
    new_bill = Bill(
        billName=data['billName']
    )
    db.session.add(new_bill)
    db.session.commit()
    return jsonify({'message': 'Bill added successfully'})


# 删除账单记录
def delete_bill(bill_id):
    bill = Bill.query.get(bill_id)
    if not bill:
        return jsonify({'error': 'Bill not found'})
    db.session.delete(bill)
    db.session.commit()
    return jsonify({'message': 'Bill deleted successfully'})


# 修改账单记录
def update_bill(bill_id):
    bill = Bill.query.get(bill_id)
    if not bill:
        return jsonify({'error': 'Bill not found'})
    data = request.get_json()
    bill.billName = data.get('billName', bill.billName)
    db.session.commit()
    return jsonify({'message': 'Bill updated successfully'})


# 获取所有账单记录
def get_bills():
    bills = Bill.query.all()
    result = []
    for bill in bills:
        result.append({
            'billId': bill.billId,
            'billName': bill.billName
        })
    return jsonify(result)
