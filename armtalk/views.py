#-*-encoding=UTF-8 -*-

from armtalk import app
from flask import render_template,redirect,request,flash,get_flashed_messages
from models import User,Image,db
import random,hashlib,json
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#解决UnicodeDecodeError: 'ascii' codec can't decode byte 0xe7 in position 0: ordinal not in range(128)
app.jinja_env.line_statement_prefix='#'
@app.route('/',methods=['GET','POST'])
def index(page=1):
    page = request.args.get('page', 1, type=int)# 通过request.args.get我们可以获取一个url所带的参数
    #request.args.get('page',1,type=int)的意思是从request的参数中获取参数page的值，如果参数不存在那么返回默认值1，type=int保证返回的默认值是整形数字。
    pagination = Image.query.paginate(page, per_page=5, error_out=False)
    #  SQLAlchemy中查询对象query的paginate方法返回一个分页对象pagination，Post.query.pagination(page，per_page=1,error_out=False)中第一个参数表示我们要查询的页数，这里用了上面获取的url的参数；第二个参数是每页显示的数量，我们这里设置成了5，如果不设置默认显示20条；第3个参数如果设置成True，当请求的页数超过了总的页数范围，就会返回一个404错误，如果设为False，就会返回一个空列表。
    image = pagination.items#当前页的对象
    #paginate()方法返回的Pagination类对象包含很多属性和方法，我们可以利用它的属性和方法实现分页导航。
    return render_template('index.html',images=image,pagination=pagination,page=page)
    #image=Image.query.order_by('id desc').limit(5).all()
   # return render_template('index.html',images=image)

@app.route('/image/<int:image_id>/')
def image(image_id):
    image=Image.query.get(image_id)
    if image==None:
        return redirect('/')#调到首页
    return render_template('pageDetail.html',image=image)

@app.route('/profile/<int:user_id>/')
@login_required#未登录无法查看个人信息
def profile(user_id):
    user=User.query.get(user_id)
    if user==None:
        return redirect('/')
    paginate=Image.query.filter_by(user_id=user_id).paginate(page=1,per_page=3,error_out=False)
    return render_template('profile.html',user=user,images=paginate.items,has_next=paginate.has_next)

@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/',methods={'post','get'})
def user_image(user_id,page,per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    map={'has_next':paginate.has_next}
    images=[]
    for image in paginate.items:
        imgvo={'id':image.id,'url':image.url,'comment_count':len(image.comments)}
        images.append(imgvo)
    map['images']=images
    return json.dumps(map)
#使用flash 返回错误信息
def redirect_with_msg(target,msg,category):
    if msg!=None:
        flash(msg, category=category)
    return redirect(target)
@app.route('/regloginpage/',methods={'post','get'})
def regloginpage(msg=''):
    for m in get_flashed_messages(with_categories=False,category_filter=['reglogin']):#消息类型过滤器
        msg=msg+m
    #未登录时，点击用户时，http://127.0.0.1:5000/regloginpage/?next=%2Fprofile%2F1%2F，出现了next
    return render_template('login.html',msg=msg,next=request.values.get('next'))


@app.route('/reg/',methods={'post','get'})
def reg():
    #request.args
    #request.form
    #获取用户名密码
    username=request.values.get('username').strip()#strip是去掉前后的空格
    password=request.values.get('password').strip()
    #print 1,username
    if username=='' or password=='':
        return redirect_with_msg('/regloginpage', '用户名和密码不能为空！', 'reglogin')
        #flash(u'用户名和密码不能为空！')
        #return redirect('/regloginpage/')
    user=User.query.filter_by(username=username).first()
    if user!=None:
        return redirect_with_msg('/regloginpage','用户名已经存在','reglogin')
        #return redirect('/')
        #flash(u'用户名已经存在！')
        #return redirect('/regloginpage/')


    salt='.'.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&*^',10))#yan
    m=hashlib.md5()
    m.update(password+salt)
    password=m.hexdigest()
    user=User(username,password,salt)
    db.session.add(user)
    db.session.commit()
    login_user(user)#注册后自动登录
    next = request.values.get('next')
    if next != None and next.startswith('/'):
        return redirect(next)
    return redirect('/')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')
@app.route('/login/',methods={'post','get'})
def login():
    # 获取用户名密码
    username = request.values.get('username').strip()  # strip是去掉前后的空格
    password = request.values.get('password').strip()
    # print 1,username
    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', '用户名和密码不能为空！', 'reglogin')
        # flash(u'用户名和密码不能为空！')
        # return redirect('/regloginpage/')
    user = User.query.filter_by(username=username).first()
    if user == None:
        return redirect_with_msg('/regloginpage', '用户名不存在！', 'reglogin')
        # return redirect('/')
        # flash(u'用户名已经存在！')
        # return redirect('/regloginpage/')
    m=hashlib.md5()
    m.update(password+user.salt)
    if (m.hexdigest()!=user.password):
        return redirect_with_msg('/regloginpage', '密码不正确！', 'reglogin')

    login_user(user)

    next=request.values.get('next')
    if next!=None and next.startswith('/'):
        return redirect(next)
    return redirect('/')







