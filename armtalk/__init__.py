#-*-encoding=UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#加载配置文件
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile('app.conf')
db=SQLAlchemy(app)#定义一个数据库

from armtalk import views,models