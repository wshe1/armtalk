#-*-encoding=UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app=Flask(__name__)
#加载配置文件
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
app.secret_key='armtalk'#初始化加密的key.
db=SQLAlchemy(app)#定义一个数据库
login_manager=LoginManager(app)#初始化
login_manager.login_view='/regloginpage/'#未登录将自动调到某个页面

from armtalk import views,models