import pymysql
#连接数据库
db = pymysql.connect('localhost','root',
                     '123456','project_all')

#创建游标对象
cursor = db.cursor()

#打开dict文件
f = open('dict.txt')

for line in f:
    tmp = line.split(' ')
    word = tmp[0]
    mean = ' '.join(tmp[1:]).strip()
    #执行sql语句
    sql = "insert into edict_project(word,mean) VALUES\
           ('%s', '%s')"%(word,mean)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

#关闭文本
f.close()

