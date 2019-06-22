'''
业务逻辑模块
    1.实现学生信息系统的操作
'''
import pymysql

#连接数据库
db = pymysql.connect('localhost','root','123456','project_all')

#创建游标对象
cursor = db.cursor()

def insert_stu():
    id = int(input('请输入学生学号：'))
    name = input('请输入学生姓名:')
    age = input('请输入学生年龄:')
    gerend = input('请输入学生性别:')
    grade = input('请输入学生年级:')
    address = input('请输入学生户籍地址:')
    score = float(input('请输入学生成绩:'))
    age = int(age)
    #编写sql语句
    sql = "insert into stu_sys(id,name,age,gerend,grade,address,score) \
          VALUES ('%d','%s','%d','%s','%s','%s','%f')"%(id,name,age,gerend,grade,address,score)
    try:
        cursor.execute(sql)
        db.commit()
        print("学生信息输入成功")
    except Exception as e:
        print(e)
        db.rollback()

def find_stu():
    id = int(input('请输入学生的学号：'))
    sql = "select * from stu_sys where id='%d'"%id
    cursor.execute(sql)
    re = cursor.fetchone()
    if re:
        print('==================================================')
        print("学生姓名:"+re[1]+'\n'+"学生年龄:"+str(re[2])+'\n'+
              "学生性别:"+re[3]+'\n'+"学生年级:"+re[4]+'\n'+
              "学生户籍:"+re[5]+'\n'+"学生分数:"+str(re[6]))
        print('==================================================')
    else:
        print("没有这个学生，请核对学号")

def delete_stu():
    id = int(input('请输入学生的学号：'))
    sql = "delete from stu_sys where id='%d'" % id
    try:
        cursor.execute(sql)
        db.commit()
        print("删除成功")
    except Exception as e:
        db.rollback()
        print(e)

def update_stu():
    id = int(input('请输入学生的学号：'))
    row = input('请输入您要修改的名称:')
    value = input('请输入你要修改的值')
    sql = "update stu_sys set '%s' = '%s' where id = '%d'"%(row,value,id)
    cmd = input('是否确认修改,Y/N?')
    if cmd == 'Y':
        try:
            cursor.execute(sql)
            db.commit()
            print('修改成功')
        except Exception as e:
            db.rollback()
            print('操作失败,原因是',e)

def total_stu():
    sql = "select gerend,count(*) from stu_sys group by gerend"
    cursor.execute(sql)
    re = cursor.fetchall()
    print("学生总人数：",re)

def order_by_stu():
    sql = "select * from stu_sys order by score"
    cursor.execute(sql)
    re = cursor.fetchall()
    for item in re:
        print(item)

def find_all_stu():
    sql = "select * from stu_sys"
    cursor.execute(sql)
    re = cursor.fetchall()
    if re:
        for item in re:
            print(item)
    else:
        print('no')
