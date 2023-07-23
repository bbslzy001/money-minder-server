# money-minder-server\models\txn_type.py

from models import db


class TxnType(db.Model):
    __tablename__ = 'txn_type'

    txn_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    txn_type_name = db.Column(db.String(100))

    # txns = db.relationship("Txn", cascade="all, delete, delete-orphan")  # 不操作 / 将对应的Txn中的rule_id字段变更为1
    rules = db.relationship("Rule", cascade="all, delete, delete-orphan")  # 一对多关系，代码级联删除

    def __init__(self, txn_type_name):
        self.txn_type_name = txn_type_name

    @staticmethod
    def insert_initial_data():
        # 检查数据库中是否已存在TxnType表的数据
        txn_type_exists = db.session.query(TxnType).first() is not None

        # 如果不存在数据，插入初始数据
        if not txn_type_exists:
            txn_types = [
                ["其他"],
                ["工资薪资", "资金借贷"],
                ["餐饮美食", "日用百货", "家具家装", "数码电器", "服饰装扮", "交通出行", "充值缴费", "医疗健康", "文化休闲",
                 "酒店旅游", "教育培训", "税务保险", "债务还款", "慈善捐赠", "宠物饲养"],
                ["理财投资", "资产买卖", "转账红包"],
            ]

            for txn_type_group in txn_types:
                for txn_type_name in txn_type_group:
                    txn_type = TxnType(txn_type_name)
                    db.session.add(txn_type)

            db.session.commit()
