#-*-encoding=UTF-8 -*-

from armtalk import app
from flask import render_template,redirect,request
from models import User,Image
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
def profile(user_id):
    user=User.query.get(user_id)
    if user==None:
        return redirect('/')
    return render_template('profile.html',user=user)

