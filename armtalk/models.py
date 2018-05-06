#-*-encoding=UTF-8 -*-
from armtalk import db
import random
from datetime import datetime
class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.String(1024))
    image_id=db.Column(db.Integer,db.ForeignKey('image.id'))#使用类名的小写
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    status=db.Column(db.Integer,default=0)#0正常，1被删除
    user=db.relationship('User')#一个评论是一个用户发胡

    def __init__(self,content,image_id,user_id):
        self.content=content
        self.image_id=image_id
        self.user_id=user_id

    def __repr__(self):
        return '<Content %d %s>' %(self.id,self.content)



class Image(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    url=db.Column(db.String(256))#图片的Url
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))#外键
    create_date=db.Column(db.DateTime)#时间
    comments=db.relationship('Comment')#内容，一张图片有多个评论

    def __init__(self,url,user_id):
        self.url=url
        self.user_id=user_id
        self.create_date=datetime.now()
    def __repr__(self):#表达
        return '<Image %d %s>' %(self.id,self.url)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)#定义id的属性，整形，逐主键，自动递增
    username=db.Column(db.String(80),unique=True)
    password=db.Column(db.String(32))
    head_url=db.Column(db.String(256))
    images=db.relationship('Image',backref='user',lazy='dynamic')#互相关联，一个人有多个图片

    def __init__(self,uname,passwd):#构造函数
        self.username=uname
        self.password=passwd
        self.head_url='https://gss2.bdstatic.com/-fo3dSag_xI4khGkpoWK1HF6hhy/baike/s%3D220/sign=ffd0c2b2bd0e7bec27da04e31f2fb9fa/810a19d8bc3eb135f52b6106a31ea8d3fc1f449b.jpg'
    def __repr__(self):#显示
        return '<User %d %s>' %(self.id,self.username)