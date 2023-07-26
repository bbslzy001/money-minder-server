# money-minder-server\services\bill_service.py

from models import db
from models.bill import Bill


def add_bill(data):
    new_bill = Bill(
        bill_name=data['billName'],
        start_date=data['startDate'],
        end_date=data['endDate'],
        bill_type=data['billType'],
    )
    db.session.add(new_bill)
    db.session.commit()
    bill_id = new_bill.bill_id  # 获取自增ID
    return {'message': 'Bill added successfully', 'id': bill_id}


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
    bill.bill_name = data.get('billName', bill.bill_name)
    bill.start_date = data.get('startDate', bill.start_date)
    bill.end_date = data.get('endDate', bill.end_date)
    bill.bill_type = data.get('billType', bill.bill_type)
    db.session.commit()
    return {'message': 'Bill updated successfully'}


def get_bills():
    bills = Bill.query.all()
    result = [{
        'billId': bill.bill_id,
        'billName': bill.bill_name,
        'startDate': bill.start_date,
        'endDate': bill.end_date,
        'billType': bill.bill_type,
    } for bill in bills]
    return {'message': 'Bill gotten successfully', 'result': result}
