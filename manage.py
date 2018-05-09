#-*-encoding=UTF-8 -*-

from armtalk import app#导入app
from flask_script import Manager
from  armtalk import db
from sqlalchemy import or_,and_#导入并和或
from armtalk.models import User,Image,Comment
import flask_mysqldb

manger=Manager(app)#通过命令行启动服务器
#通过系统最 最初时相间数据库初始化，python python manage.py init_databas
@manger.command
def init_databas():#定义自己的相关的命令。,装饰器，能在命令行中运行。
    db.drop_all()
    db.create_all()#根据models胡数据表在数据库中创建表
    for i in range(1,20):
        db.session.add(User('user'+str(i),'123456'))#添加数据
        for j in range(0,10):
            db.session.add(Image('http://www.haijun360.com/china/117/images/1x.jpg',i))
            for k in range(0,3):#数据库的id必须在从1开始。
                db.session.add(Comment('abcdef',i*2+j-1,i))
    db.session.commit()
    #修改
    for i in range(10,18,2):
        user=User.query.get(i)
        user.username='new'+user.username
    User.query.filter_by(id=11).update({'username':'New2'})

    db.session.commit()
    #删除
    for i in range(30,50,2):
        comment=Comment.query.get(i+1)
        db.session.delete(comment)
    db.session.commit()


    print 1,User.query.all()#查询所有
    print 2,User.query.get(2)#查询第二个用户
    print 3,User.query.filter_by(id=5).first()#条件查询，id=5
    print 4,User.query.order_by(User.id.desc()).offset(1).limit(2).all()#降序排列，偏移一个（从倒数第二个开始）输出2个。select * from user order by id desc limit 1,2;
    print 5,User.query.filter(User.username.endswith('0')).limit(3).all()
    print 6,User.query.filter(or_(User.id==5, User.id==15)).all()#或操作，去掉all()就能看到SQL 语句
    print 7,User.query.filter(and_(User.id>=6,User.id<11)).all()
    print 8, User.query.filter(and_(User.id >= 6, User.id < 11)).first_or_404()
    #分页
    print 9,User.query.order_by(User.id.desc()).paginate(page=1,per_page=5).items
    #关联查询，由于在Model中指定的了，images和Image的表关联的。当用到胡时候会自己去查，根据image种ForeingKey关联去查
    user=User.query.get(1)#获得一个用户
    print 10,user.images.all()#需要加all()
    image=Image.query.get(1)#获得一个图片
    print 11,image.user#获得一个一张图片的用户


if __name__=='__main__':
    manger.run()