#电子词典服务端
#coding:utf8
'''
服务端功能介绍：
1.和客户端tcp套接字进行连接
2.接受客户端请求
3.将查询到的结果返回给客户端
'''
from socket import *
import pymysql
import signal
import sys,os
import time

POST = "127.0.0.1"
HOST = 8800
ADDRESS = (POST,HOST)
DICT_TEXT = './dict.txt'

#连接数据库
db = pymysql.connect('localhost','root','123456','project_all')

#创建游标对象
cursor = db.cursor()


def do_request(connfd):
    #接收客户端发送的数据
    while True:
        data = connfd.recv(1024).decode()
        print(data)
        if not data or data[0] == 'E':
            '''如果接收数据为空或者第一个数据是E,则关闭套接字'''
            connfd.close()
            return
        elif data[0] == 'R':
            do_regist(data,connfd)
        elif data[0] == 'L':
            do_login(data,connfd)
        elif data[0] == "S":
            do_select_word(connfd,data)
        elif data[0] == 'H':
            do_selet_history(connfd,data)

def do_login(data,connfd):
    tmp = data.split(' ')
    name = tmp[1]
    pwd = tmp[2]
    sql = "select * from user where name='%s' and pwd = '%s'"\
          %(name,pwd)
    cursor.execute(sql)
    re = cursor.fetchone()
    if re:
        connfd.send(b'OK')
    else:
        connfd.send('账号或密码错误，请重新输入'.encode())

def do_regist(data,connfd):
    tmp = data.split(' ')
    name = tmp[1]
    pwd = tmp[2]
    #数据库查询
    sql = "select * from user WHERE name='%s'"%(name)
    cursor.execute(sql)
    #返回查询结果
    re = cursor.fetchone()
    if re != None:
        connfd.send('该用户已存在'.encode())
        return
    else:
        #插入数据库
        sql = "insert into user(name,pwd) values('%s','%s')"\
              %(name,pwd)
        try:
            cursor.execute(sql)
            db.commit()
            connfd.send(b'OK')
        except:
            db.rollback()
            connfd.send('注册失败'.encode())

def do_select_word(connfd,data):
    tmp = data.split(' ')
    word = tmp[1]
    name = tmp[2]
    tm = time.ctime()
    tm = str(tm)
    #插入历史记录表
    sql = "insert into history(name,word,time) values('%s','%s','%s')"%(name,word,tm)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    #查询单词
    sql = "select mean from edict_project \
          where word = '%s'"%word
    cursor.execute(sql)
    re= cursor.fetchone()
    if re:
        re = str(re)
        re = re[1:-1]
        connfd.send(re.encode())
    else:
        connfd.send(b'NO find')

def do_selet_history(connfd,data):
    tmp = data.split(' ')
    name = tmp[1]
    sql = "select * from history where name='%s' order by id limit 5"%name
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    re = cursor.fetchall()
    if re:
        connfd.send(b'OK')
        for i in re:
            msg = "%s %s %s"%(i[1],i[2],i[3])
            print(msg)
            time.sleep(0.1)
            connfd.send(msg.encode())
        time.sleep(0.2)
        connfd.send(b'**')
    else:
        connfd.send(b"NO")
        return


#搭建网络连接
def main():
    #创建套接字
    server_socket = socket()
    #设置端口复用
    server_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #绑定地址
    server_socket.bind(ADDRESS)
    #设置监听
    server_socket.listen(5)
    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    #循环等待连接
    while True:
        try:
            connfd,addr = server_socket.accept()
            print("connect from",addr)
        except KeyboardInterrupt:
            server_socket.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
    #创建子进程
        pid = os.fork()
        if pid < 0:
            print("创建进程失败")
        elif pid == 0:
            #子进程处理客户端请求
            server_socket.close()
            do_request(connfd)
            sys.exit()
        else:
            #父进程关闭
            connfd.close()


if __name__ == "__main__":
    main()