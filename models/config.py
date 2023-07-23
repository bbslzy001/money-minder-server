# money-minder-server\models\config.py

from models import db


class Config(db.Model):
    __tablename__ = 'config'

    config_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    config_name = db.Column(db.String(100))
    config_value = db.Column(db.JSON)

    def __init__(self, config_name, config_value):
        self.config_name = config_name
        self.config_value = config_value

    @staticmethod
    def insert_initial_data():
        # 检查数据库中是否已存在Config表的数据
        config_exists = db.session.query(Config).first() is not None

        # 如果不存在数据，插入初始数据
        if not config_exists:
            configs = [
                ["ruleRequest", {
                    "addRuleApplyTxns": True,
                    "deleteRuleApplyTxns": False,
                    "updateRuleApplyTxns": True,
                }],
            ]

            for config in configs:
                config = Config(config[0], config[1])
                db.session.add(config)

            db.session.commit()
