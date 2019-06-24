#! /usr/bin/env python3
from flask import Flask,request,render_template,redirect,Response,session,make_response
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from sqlalchemy import and_
import json
#创建app对象
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost:3306/middle_project"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

app.config["DEBUG"]= True

app.config['SECRET_KEY'] = '123456'

db = SQLAlchemy(app)

manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command("db",MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(50),nullable=True,unique=True)
    pwd = db.Column(db.String(120),nullable=True)
    email = db.Column(db.String(120),nullable=True)
    tel = db.Column(db.String(20),nullable=True)
    isactive = db.Column(db.Boolean)
    movierank01 = db.Column(db.Integer,nullable=True)
    movierank02 = db.Column(db.Integer,nullable=True)
    movierank03 = db.Column(db.Integer,nullable=True)
    movierank04 = db.Column(db.Integer,nullable=True)
    movierank05 = db.Column(db.Integer,nullable=True)
    movierank06 = db.Column(db.Integer,nullable=True)
    movierank07 = db.Column(db.Integer,nullable=True)
    movierank08 = db.Column(db.Integer,nullable=True)
    movierank09 = db.Column(db.Integer, nullable=True)
    movierank10 = db.Column( db.Integer,nullable=True)
    index_moviename = db.Column(db.String(200),nullable=True)



class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50)) #电影名称
    director = db.Column(db.String(50)) #导演
    rate = db.Column(db.String(50))#评分
    caste = db.Column(db.String(200))#主演
    movie_poster = db.Column(db.String(200))#海报
    movie_review = db.Column(db.Text)#简介
    area = db.Column(db.String(50))#地区


class Pearson(db.Model):
    __tablename__ = "pearson"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    index_moviename = db.Column(
        db.String(300),
        nullable=True
    )

    movierank01 = db.Column(
        db.String(120),
        nullable=True
    )

    movierank02 = db.Column(
        db.String(120),
        nullable=True
    )

    movierank03 = db.Column(
        db.String(120),
        nullable=True
    )

    movierank04 = db.Column(
        db.String(120),
        nullable=True
    )

    movierank05 = db.Column(
        db.String(120),
        nullable=True
    )

    movierank06 = db.Column(
        db.String(120),
        nullable=True
    )

    movierank07 = db.Column(
        db.String(120),
        nullable=True
    )

    movierank08 = db.Column(
        db.String(120),
        nullable=True
    )

    movierank09 = db.Column(
        db.String(120),
        nullable=True
    )

    movierank10 = db.Column(
        db.String(120),
        nullable=True
    )

user_msg = []
ulist = []

def checkmsg(uname,upwd):
    user = User.query.filter_by(uname=uname).first()
    #如果用户名在数据库
    if user:
        #验证密码
        if upwd == user.pwd:
            #如果密码正确
            return True
        #如果密码不正确
        else:
            return False
    #如果用户名不在数据库
    else:
        return False

def checkcookie(page):
    # 如果没有session，但cookies里有用户信息
    if 'uname' in request.cookies:
        uname = request.cookies['uname']
        upwd = request.cookies['upwd']
        # 验证用户名密码是否正确
        res = checkmsg(uname, upwd)
        # 如果用户名密码正确,存入session,进入要进入的下一页
        if res:
            session['uname'] = uname
            session['upwd'] = upwd
            return redirect('/' + page+"?uname="+uname)
        # 如果用户名密码不正确，清除cookies，返回登录页面
        else:
            resp = make_response(redirect('/login'))
            resp.delete_cookie('uname')
            resp.delete_cookie('upwd')
            return resp
    # 如果没有session，cookies里也没有用户信息
    else:
        print("没有检查到cookies")
        return redirect('/login')

@app.route("/")
def index():
    return render_template("first-page.html")

@app.route("/01-search",methods=["POST"])
def search():
    if request.method == "POST":
        name = request.form["move_name"]
        re = Move.query.filter_by(title=name).first()
        if re:
            print(re.movie_review)
            return render_template("show.html",re=re)

@app.route("/02_reg",methods=["GET","POST"])
def reg():
    if request.method == "GET":
        return  render_template("regiest.html")
    else:
        user = User()
        # print(request.form)
        user.uname = request.form.get("uname")
        user.pwd = request.form.get("upwd")
        user.email = request.form.get("uemail")
        user.tel = request.form.get("utel")
        user.isactive = False
        if request.form.get("active"):
            user.isactive = True
        if user.uname and user.pwd and user.email and user.email and user.tel and user.isactive:
            try:
                db.session.add(user)
                return json.dumps({"status": 1})
            except Exception as e:
                print(e)
        else:
            json.dumps({"status": 0})

@app.route("/02_regserver",methods=["POST"])
def regserver():
    uname = request.form.get("uname")

    if User.query.filter_by(uname=uname).first():
        return json.dumps({"status": 0})
    else:
        return json.dumps({"status": 1})

@app.route('/checklogin')
def checklogin():
    page = request.args['page']
    print(page)
    # 如果有session
    if session:
        #如果用户信息在session里,进入要进入的下一页
        try:
            uname = session['uname']
            return redirect("/"+page+"?uname="+uname)
        except:
            return redirect('/login?page='+page)
    #如果没有session,检查cookie
    else:
        print("开始检查cookies")
        # 如果没有session，但cookies里有用户信息
        if 'uname' in request.cookies:
            uname = request.cookies['uname']
            upwd = request.cookies['upwd']
            # 验证用户名密码是否正确
            res = checkmsg(uname, upwd)
            # 如果用户名密码正确,存入session,进入要进入的下一页
            if res:
                session['uname'] = uname
                session['upwd'] = upwd
                user=User.query.filter_by(uname=uname).first()
                id=user.id
                print(id)
                session['id']=str(id)
                return redirect('/' + page + "?uname=" + uname)
            # 如果用户名密码不正确，清除cookies，返回登录页面
            else:
                resp = make_response(redirect('/login'))
                resp.delete_cookie('uname')
                resp.delete_cookie('upwd')
                return resp
        # 如果没有session，cookies里也没有用户信息
        else:
            print("没有检查到cookies")
            return redirect('/login')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="GET":
        if 'uname' in session:
            uname = session['uname']
            return render_template('first-page.html',locals())
        else:
            return render_template('logoin.html')
    else:
        uname=request.form['uname']
        upwd=request.form['upwd']
        # isActive=request.form['isActive']
        # print("isActive:",isActive)
        print("登录的用户密码是",uname,upwd)
        #验证账号密码是否正确
        res = checkmsg(uname, upwd)
        print("账号密码验证结果是",res)
        #账号密码正确
        if res:
            #验证成功存入session
            session['uname'] = uname
            session['upwd'] = upwd
            user = User.query.filter_by(uname=uname).first()
            id = user.id
            print(id)
            session['id']=id

            #是否记住密码
            if 'isActive' in request.form:
                resp = make_response(redirect('/'))
                resp.set_cookie("uname", uname)
                resp.set_cookie("upwd", upwd)
                return resp
            #不记住密码直接返回首页
            else:
                return redirect('/')
        #账号密码错误,返回登录页面
        else:
            # dic={'text':'账号密码错误，请重新输入'}
            # return json.dumps(dic)
            tip = "账号密码错误 请重新输入"
            return render_template('logoin.html',tip=tip)

@app.route('/getsession')
def getsession():
    if 'uname' in session:
        uname=session['uname']
        id=session['id']
        print(id)
        print("uname:",uname)
    else:
        print("session中没有uname")
    return "取出session数据成功"

@app.route('/04-more',methods=["GET",'POST'])
def more():
    if request.method == "GET":
        return render_template('chine-move.html')

@app.route('/05-more',methods=["GET",'POST'])
def more1():
    return render_template('###.html')

@app.route('/06-about')
def about():
    return render_template("aboutus.html")

@app.route("/07-privacy")
def privacy():
    return render_template("privacy-policy.html")

@app.route('/history')
def history():
    return render_template("history.html")

@app.route('/member')
def member():
    id = session['id']
    user = User.query.filter_by(id=id).first()
    return render_template("member.html",user=user)

@app.route('/set')
def set():
    return render_template("set.html")

@app.route('/update')
def update():
    return render_template("update.html")

@app.route("/recommend",methods=["GET",'POST'])
def recommend():
    if request.method == "GET":
        return render_template("recommend.html")
    else:
        pass

@app.route('/info',methods=["POST","GET"])
def info():
    if request.method == "GET":
        id = session['id']
        user = User.query.filter_by(id=id).first()
        return render_template("info.html",user=user)
    else:
        id = request.form['id']
        name = request.form['uname']
        user = User.query.filter_by(id = id).first()
        user.uname = request.form['uname']
        user.pwd = request.form['upwd']
        user.email = request.form['email']
        user.tel = request.form['phone']
        db.session.add(user)
        return render_template("info.html",user = user)

@app.route("/01-add",methods=['GET','POST'])
def add_views():
    #1.创建Users的对象并赋值
    if request.method == 'GET':
        return render_template('recommend.html')
    else:
        resp = session['id']
        print(resp)
        User1 = User.query.filter_by(id=resp).first()
        User1.movierank01 = request.form['A1']
        User1.movierank02 = request.form['A2']
        User1.movierank03 = request.form['A3']
        User1.movierank04 = request.form['A4']
        User1.movierank05 = request.form['A5']
        User1.movierank06 = request.form['B1']
        User1.movierank07 = request.form['B2']
        User1.movierank08 = request.form['B3']
        User1.movierank09 = request.form['B4']
        User1.movierank10 = request.form['B5']
        db.session.add(User1)
        return redirect('/02-query')

@app.route('/02-query')
def calcuate():
    result = []
    final = []
    final_dict = []
    if request.method == 'GET':
        User_id = session['id']
        y = User.query.filter_by(id=User_id).first()
        l1 = [y.movierank01,y.movierank02,y.movierank03,y.movierank04,y.movierank05,y.movierank06,y.movierank07,y.movierank08,y.movierank09,y.movierank10]
        matrix_l1 = np.array(l1)
        x = Pearson.query.all()
        for row in range(9560):
            l2 = [float(x[row].movierank01),float(x[row].movierank02),float(x[row].movierank03),float(x[row].movierank04),float(x[row].movierank05),float(x[row].movierank06),float(x[row].movierank07),float(x[row].movierank08),float(x[row].movierank09),float(x[row].movierank10)]
            matrix_l2 = np.array(l2)
            matrix_l2 = np.where(matrix_l2 > 0.3,matrix_l2,0)
            sum_final = np.dot( matrix_l2,matrix_l1.T)
            sum_final = sum_final/sum(l2)
            final.append(sum_final)
        for index,value in enumerate(final):
            if value >=3:
                final_dict.append(index + 1)
        if len(final_dict) == 0:
            return '查询失败'
        elif len(final_dict) <= 10:
            final_dict = final_dict
        else:
            final_dict = final_dict[:10]
        for index_moviename in final_dict:
            x = Pearson.query.filter(Pearson.id == index_moviename).all()
            result.append(x[0].index_moviename)
        return render_template('query.html',result = result)

@app.route('/forginer')
def forginer():
    return render_template('videonow.html')

@app.route('/videold')
def videomow():
    return render_template('videoold.html')

@app.route('/viedowill')
def viesowill():
    return render_template('videowill.html')











if __name__ == "__main__":
    manager.run()
