# money-minder-server\services\bill_service.py

from models import db
from models.bill import Bill


def add_bill(data):
    new_bill = Bill(
        billName=data['billName']
    )
    db.session.add(new_bill)
    db.session.commit()
    bill_id = new_bill.billId  # 获取自增ID
    return {'message': 'Bill added successfully', 'billId': bill_id}


def delete_bill(bill_id):
    bill = Bill.query.get(bill_id)
    if not bill:
        return {'error': 'Bill not found'}
    db.session.delete(bill)
    db.session.commit()
    return {'message': 'Bill deleted successfully'}


def update_bill(bill_id, data):
    bill = Bill.query.get(bill_id)
    if not bill:
        return {'error': 'Bill not found'}
    bill.billName = data.get('billName', bill.billName)
    db.session.commit()
    return {'message': 'Bill updated successfully'}


def get_bills():
    bills = Bill.query.all()
    result = []
    for bill in bills:
        result.append({
            'billId': bill.billId,
            'billName': bill.billName
        })
    return result
