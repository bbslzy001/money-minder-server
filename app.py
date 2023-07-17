# money_minder_server\app.py

import os
from flask import Flask
from flask_cors import CORS
from models.txn import db
from views.init import api_blueprint


def create_app():
    # 创建Flask应用
    app = Flask(__name__)

    # 加载配置
    environment = os.environ.get('FLASK_ENV', 'development')  # 默认为开发环境
    app.config.from_pyfile(f'settings/{environment}.py')

    # 根据配置决定是否启用调试模式
    app.debug = app.config['DEBUG']

    # 根据配置决定是否启用跨域功能
    if app.config['ENABLE_CORS']:
        CORS(app)

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(api_blueprint)

    return app


# 启动Flask
if __name__ == '__main__':
    my_app = create_app()
    my_app.run()
