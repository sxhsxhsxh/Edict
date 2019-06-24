import numpy as np
import pandas as pd
from math import *
import pymysql
rating_list = pd.read_csv('static/ml-latest-small/ratings.csv')
movie_list = pd.read_csv('static/ml-latest-small/movies.csv')


def create_dict():
    index = 0
    user = {}
    for i in range(1, 611):
        dict_movie = {}
        for index, row in rating_list.loc[index:, 'userId':'rating'].iterrows():
            if int(row['userId']) == i:
                movieId = int(row['movieId'])
                dict_movie[movieId] = row['rating']
                index += 1
            else:
                user[i] = dict_movie
                break
    return user


def movieId():
    dict_02 = {}
    for index, row in movie_list.iloc[:, 0:2].iterrows():
        dict_02[row['movieId']] = row['title']
    return dict_02


def pearson(Z, p1, p2):
    '''
    计算皮尔逊相关系数
    :param Z: PCA矩阵
    :param p1: 电影１
    :param p2: 电影２
    :return:
    '''
    n = 491
    sum1 = np.sum(Z[p1][:])
    sum2 = np.sum(Z[p2][:])

    psum = np.sum(Z[p1][:] * Z[p2][:])

    sum1sq1 = sum([pow(x, 2) for x in Z[p1][:]])
    sum2sq2 = sum([pow(x, 2) for x in Z[p2][:]])

    num = psum - (sum1 * sum2 / n)
    den = np.sqrt((sum1sq1 - pow(sum1, 2) / n) * (sum2sq2 - pow(sum2, 2) / n))

    if den == 0: return 0
    r = num / den
    return r


def index_get(dataFrame, movieId_list):
    '''

    :param dataFrame: 电影dataframe格式
    :param movieId_list: 电影index + 1列表
    :return:
    '''
    l = []
    for i in movieId_list:
        x = dataFrame[dataFrame['movie'] == i]
        l.append(x.index[0] + 1)
    return l


def pearson_dict(Z, movieId_list, pearson=pearson):
    '''
    循环求出相关系数
    :param Z:
    :param movieId_list:
    :param pearson:
    :return:
    '''
    list_x = []
    for x in movieId_list:
        dict01 = {}
        for y in range(9562):
            if x == y:
                continue
            dict01[y] = pearson(Z, x, y)
        list_x.append(dict01)
    return list_x


dict_moviename = movieId()
moviename = pd.Series(dict_moviename)
moviename = pd.DataFrame(moviename, columns=['moviename'])
moviename.insert(0, 'index', moviename.index)  # 构建movieid 与 moviename　dataframe

dict_movie = create_dict()
pdData = pd.DataFrame(dict_movie)
pdData = pdData.fillna(0)
arr01 = []
for index, row in pdData.iterrows():
    arr01.append(index)
pdData['index'] = arr01
pdData.insert(0, 'movie', pdData.pop('index'))  # 构建movieid与评分的dataframe

pdData = pd.merge(pdData, moviename, left_on='movie', right_on='index')  # 对应movieid　与电影名称
pdData.insert(1, 'moviename', pdData.pop('moviename'))  # 重建列索引
del pdData['index']  # 删除多余列

moviename_list = pdData.moviename

l1 = []
for index, row in pdData.iterrows():
    l2 = []
    for x in row:
        l2.append(x)
    l1.append(l2)
matrix = np.array(l1)
matrix_cal = matrix[:, 2:]
matrix_cal = matrix_cal.astype(np.float64)
mean = matrix_cal.mean(axis=0)
norm = matrix_cal - mean
scope = np.max(norm, axis=0) - np.min(norm, axis=0)
norm = norm / scope
u, s, v = np.linalg.svd(np.dot(norm.T, norm))  # PCA降维
U_reduce = u[:, :491]
pdData_reduce = np.dot(matrix_cal, U_reduce)

index_list = index_get(pdData, [318, 7153, 122912, 134130, 166528, 179135, 180031, 183011, 188751, 193583])
print_x = pearson_dict(pdData_reduce, index_list)
list_01 = ['肖生克的救赎', '指环王：王者归来', '复仇者联盟：终局之战', '火星救援', '星球大战：最后的绝地武士', '蓝色星球2', '水形物语', '通勤营救', '妈妈咪呀2', '游戏人生：零']
pd_final = pd.DataFrame(print_x)
pd_final = pd_final.transpose()
pd_final.columns = list_01
pd_final = pd_final.fillna(0)
pd_final.reindex(moviename_list)
pd_final.insert(0, 'index', moviename_list)
pd_final.set_index('index', inplace=True)


db = pymysql.connect('localhost','root','123456','middle_project')
cursor = db.cursor()
insert = """insert into pearson(index_moviename,movierank01,movierank02,movierank03,movierank04,movierank05,movierank06,movierank07,movierank08,movierank09,movierank10) values
          (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
for index, row in pd_final.iterrows():
    try:
        index_moviename = row.name
        movierank01 = str(row.values[0])
        movierank02 = str(row.values[1])
        movierank03 = str(row.values[2])
        movierank04 = str(row.values[3])
        movierank05 = str(row.values[4])
        movierank06 = str(row.values[5])
        movierank07 = str(row.values[6])
        movierank08 = str(row.values[7])
        movierank09 = str(row.values[8])
        movierank010 = str(row.values[9])
        values = (index_moviename,movierank01,movierank02,movierank03,movierank04,movierank05,movierank06,movierank07,movierank08,movierank09,movierank010)
        cursor.execute(insert,values)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
cursor.close()
db.close()

