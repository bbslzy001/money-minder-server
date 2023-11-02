# money-minder-server\app.py

import os

from flask import Flask, render_template
from flask_cors import CORS
# from waitress import serve

import models  # 显式导入models模块，以便SQLAlchemy能够初始化所有模型
from models import db
from models.config import Config
from models.txn_type import TxnType
from views import api_blueprint, upload_view


def create_app():
    # 创建Flask应用
    app = Flask(__name__)

    # 加载配置
    environment = os.environ.get('FLASK_ENV', 'development')  # 默认为开发环境
    # environment = os.environ.get('FLASK_ENV', 'production')  # 默认为开发环境
    app.config.from_pyfile(f'settings/{environment}.py')

    # 根据配置决定是否启用跨域功能
    if app.config['ENABLE_CORS']:
        CORS(app)

    # 初始化数据库
    db.init_app(app)

    # 激活应用上下文并创建数据库表
    with app.app_context():
        db.create_all()
        # 在数据库中插入初始数据
        Config.insert_initial_data()
        TxnType.insert_initial_data()

    # 注册蓝图
    app.register_blueprint(api_blueprint)

    # 创建上传文件夹
    if not os.path.exists(upload_view.UPLOAD_FOLDER):
        os.makedirs(upload_view.UPLOAD_FOLDER)

    # 当Vue项目使用History模式时，刷新非根目录下的页面会发生404
    # 该问题是由于刷新页面时，浏览器向服务器请求该地址，但服务器上并没有对应路由造成的
    # 通过为Flask服务器配置"catch-all"路由，来匹配所有没有被其他路由匹配的URL，并返回index.html页面
    # 返回index.html页面后，Vue路由会在前端接管，根据URL渲染正确的组件
    # 注意：当Vue无法处理该URL时，仍然会显示空白页面或404页面
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template("index.html")

    return app


# 启动Flask
if __name__ == '__main__':
    my_app = create_app()
    # my_app.run(threaded=True)
    my_app.run(threaded=True, host='0.0.0.0', port=5000)  # 指定主机和端口（0.0.0.0表示所有可用的网络接口）
