#电子词典客户端
#coding:utf8
# 客户端功能介绍：
# 1.和服务端tcp套接字进行连接
# 2.向服务端发送请求
# 3.接收服务端发送的数据

from socket import *
import sys,os

HOST = '127.0.0.1'
PORT = 8800
ADDRESS = (HOST,PORT)

# 创建套接字
client_socket = socket()
# 设置连接
try:
    client_socket.connect(ADDRESS)
    print('ok')
except Exception as e:
    print(e)
    sys.exit()

def do_login():
    name = input('请输入姓名')
    pwd = input('请输入密码')
    msg = 'L %s %s'%(name,pwd)
    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode()
    if data == 'OK':
        to_second(name)

    else:
        print(data)

def do_regist():
    while True:
        name = input('请输入姓名')
        pwd = input('请输入密码')
        msg = 'R %s %s' % (name, pwd)
        # 发送数据
        client_socket.send(msg.encode())
        # 接收服务端消息
        data = client_socket.recv(1024).decode()
        if data == "OK":
            to_second()
        else:
            print(data)

def do_select_word(name):
    word = input("请输入单词:")
    msg = 'S %s %s'%(word,name)
    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode()
    print(data)

def do_select_history(name):
    msg = 'H %s'%name
    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode()
    if data == 'OK':
        while True:
            data1 = client_socket.recv(1024).decode()
            if data1 == "**":
                break
            print(data1)

    else:
        print(data)

#进入二级界面
def to_second(name):
    '''二级界面,功能:查询单词,查询历史,注销'''
    while True:
        print("===============================")
        print("1.查询单词    2.查看历史　　3.退出")
        print("===============================")
        cmd = input("请输入命令选项:")
        if cmd not in ["1","2","3"]:
            print("命令选项错误，请输入正确的命令符")
        elif cmd == "1":
            do_select_word(name)
        elif cmd == "2":
            do_select_history(name)
        elif cmd == "3":
            return

def main():

    #设置一级界面
    while True:
        print('============================')
        print('1.login   2.regist    3.exit')
        print('============================')
        cmd = input('请输入选项')
        if cmd not in ["1",'2','3']:
            print('请输入正确选项')
        elif cmd == '1':
            do_login()
        elif cmd == '2':
            do_regist()
        elif cmd == '3':
            client_socket.send(b'E')
            sys.exit()


if __name__ == "__main__":
    main()