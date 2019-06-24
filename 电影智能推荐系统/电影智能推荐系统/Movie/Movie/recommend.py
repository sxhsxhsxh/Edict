#! /usr/bin/env python3
from flask import Flask,render_template,request
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd
from math import *
rating_list = pd.read_csv('static/ml-latest-small/ratings.csv')
movie_list = pd.read_csv('static/ml-latest-small/movies.csv')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@127.0.0.1:3306/recommend"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DEBUG'] = True

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )



    movierank01 = db.Column(
        db.Integer,
        nullable=True
    )

    movierank02 = db.Column(
        db.Integer,
        nullable=True
    )

    movierank03 = db.Column(
        db.Integer,
        nullable=True
    )

    movierank04 = db.Column(
        db.Integer,
        nullable=True
    )

    movierank05 = db.Column(
        db.Integer,
        nullable=True
    )

    movierank06 = db.Column(
        db.Integer,
        nullable=True
    )

    movierank07 = db.Column(
        db.Integer,
        nullable=True
    )

    movierank08 = db.Column(
        db.Integer,
        nullable=True
    )

    movierank09 = db.Column(
        db.Integer,
        nullable=True
    )

    movierank10 = db.Column(
        db.Integer,
        nullable=True
    )

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





@app.route("/01-add",methods=['GET','POST'])
def add_views():
    #1.创建Users的对象并赋值
    if request.method == 'GET':
        return render_template('recommend.html')
    else:
        movie = Movie()
        movie.movierank01 = request.form['A1']
        movie.movierank02 = request.form['A2']
        movie.movierank03 = request.form['A3']
        movie.movierank04 = request.form['A4']
        movie.movierank05 = request.form['A5']
        movie.movierank06 = request.form['B1']
        movie.movierank07 = request.form['B2']
        movie.movierank08 = request.form['B3']
        movie.movierank09 = request.form['B4']
        movie.movierank10 = request.form['B5']
        db.session.add(movie)
        return "增加数据成功"

@app.route('/02-query')
def calcuate():
    result = []
    final = []
    final_dict = []
    if request.method == 'GET':
        y = Movie.query.filter(Movie.id == 5).all()
        l1 = [y[0].movierank01,y[0].movierank02,y[0].movierank03,y[0].movierank04,y[0].movierank05,y[0].movierank06,y[0].movierank07,y[0].movierank08,y[0].movierank09,y[0].movierank10]
        matrix_l1 = np.array(l1)
        x = Pearson.query.all()
        for row in range(9560):
            l2 = [float(x[row].movierank01),float(x[row].movierank02),float(x[row].movierank03),float(x[row].movierank04),float(x[row].movierank05),float(x[row].movierank06),float(x[row].movierank07),float(x[row].movierank08),float(x[row].movierank09),float(x[row].movierank10)]
            matrix_l2 = np.array(l2)
            matrix_l2 = np.where(matrix_l2 > 0.4,matrix_l2,0)
            sum_final = np.dot( matrix_l2,matrix_l1.T)
            sum_final = sum_final/sum(l2)
            final.append(sum_final)
        for index,value in enumerate(final):
            if value >=3:
                final_dict.append(index + 1)
        if len(final_dict) == 0:
            return '查询失败'
        elif len(final_dict) <= 30:
            final_dict = final_dict
        else:
            final_dict = final_dict[:30]
        for index_moviename in final_dict:
            x = Pearson.query.filter(Pearson.id == index_moviename).all()
            result.append(x[0].index_moviename)
        return render_template('query.html',result = result)

if __name__ == '__main__':
    manager.run()

