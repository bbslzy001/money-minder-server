# money_minder_server\settings\production.py

DEBUG = False  # 关闭调试模式
ENABLE_CORS = False  # 不允许跨域
SQLALCHEMY_DATABASE_URI = 'sqlite:///money_minder_production.db'  # 生产环境下的数据库文件的路径
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭对模型修改的监控
SQLALCHEMY_ECHO = False  # 不显示SQLAlchemy的Debug信息
