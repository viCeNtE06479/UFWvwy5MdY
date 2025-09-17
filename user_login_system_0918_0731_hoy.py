# 代码生成时间: 2025-09-18 07:31:02
# user_login_system.py

"""
用户登录验证系统
"""

import celery
from celery import Celery
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

# 初始化Celery
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # 配置Redis作为消息代理
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# 初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# 定义用户模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# 初始化Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# 用户登录验证任务
@celery.task
def user_login(username, password):
    """
    用户登录验证任务
    :param username: 用户名
    :param password: 密码
    :return: 登录成功或失败的提示信息
    """
    try:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return 'Login successful'
        else:
            return 'Invalid username or password'
    except Exception as e:
        return f'Error: {str(e)}'

# 用户登录接口
@app.route('/login', methods=['POST'])
def login():
    """
    用户登录接口
    :return: 登录结果
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        abort(400, description='Missing username or password')
    username = data['username']
    password = data['password']
    result = user_login.apply_async(args=(username, password)).get()
    return jsonify(result=str(result))

# 数据库初始化
@app.before_first_request
def initialize_database():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
