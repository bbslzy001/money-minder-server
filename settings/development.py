# money-minder-server\settings\development.py

ENABLE_CORS = True  # 允许跨域
SQLALCHEMY_DATABASE_URI = 'sqlite:///money_minder_development.db'  # 开发环境下的数据库文件的路径
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭对模型修改的监控
SQLALCHEMY_ECHO = True  # 显示SQLAlchemy的Debug信息
