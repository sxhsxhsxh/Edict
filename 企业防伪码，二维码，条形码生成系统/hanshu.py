import os
import tkinter
from main import *
import tkinter.messagebox

#初始化数据
number = '0123456789'
letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
allis = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@!#$%^&*()_+'
i = 0
randstr = []
fourth = []
fifth = []
randfir = ''
randsec = ""
randthr = ""
str_one = ""
strone = ""
strtow = ""
nextcard = ""
userput =""
nres_letter = ""


def mkdir(path):
    '''创建文件夹'''
    isexists = os.path.exists(path)
    if not isexists:
        os.mkdir(path)

def openfile(filename):
    '''读取文件信息'''
    f = open(filename)
    f_list = f.read()
    f.close()
    return f_list

def input_box(showstr,showerder,length):
    '''
    对数字，字母，位数验证
    :param showstr: 输入内容提示文字
    :param showerder: 参数为１，类型为数字，位数不受限制;参数为２时，类型为字母，位数由length决定;参数为３时，类型为数字,位数由length决定
    :param length: 输入内容的长度
    '''
    instr = input(showstr) #使用input函数要求用户输入信息
    if len(instr) != 0:
        if showerder == 1: #如果类型为数字
            if str.isdigit(instr):#验证是否为数字
                if instr == 0:
                    print("输入为0，请重新输入")
                    return '0'
                else:
                    return instr
            else:#如果输入的不是数字　
                print("输入非法，请重新输入")
                return '0'
        elif showerder == 2: #类型为字母:
            if str.isalpha(instr):#验证是否为字母
                if len(instr) != length:#判断输入的位数
                    print("必须输入%d个字母，长度不对，请重新输入"%length)
                    return '0'
                else:
                    return instr
            else:
                print('输入内容类型不对，请重新输入')
                return  '0'
        elif showerder == 3:
            if str.isdigit(instr):
                if len(instr) != length:#如果长度不等于指定位数
                    print("必须输入%d个字母，长度不对，请重新输入" % length)
                    return '0'
                else:
                    return instr
            else:
                print('输入内容类型不对，请重新输入')
                return '0'
    else:
        print("输入长度不能为空,请重新输入")
        return '0'

def wfile(sstr,sfile,typeis,smsg,datapath):
    '''

    :param sstr: 生成的防伪码
    :param sfile: 保存防伪码的文件名
    :param typeis: 是否显示输出完成的信息提示框
    :param smsg: 提示框提示的内容
    :param datapath: 保存防伪码的路径
    :return:
    '''
    mkdir(datapath)#调用mkdir()函数
    datafile = datapath + '\\'+sfile#设置保存防伪码的文件
    print(datafile)
    file = open(datafile,'w')#打开保存防伪码的文件,如果文件不存在，则创建该文件
    wrlist = sstr#将防伪码信息赋值给wrist
    pdata = ''
    wdata = ''
    for i in range(len(wrlist)):
        #删除字符的括号
        wdata = str(wrlist[i].replace('[','')).replace(']','')
        #删除字符的引号
        wdata = wdata.replace(''''','').replace(''''', '')
        try:
            file.write(wdata)
        except Exception as e:
            print(e)
        pdata = pdata+wdata
    file.close()
    if typeis != 'no':
        #是否显示信息提示框
        tkinter.messagebox.showinfo('提示',
                 smsg+str(len(randstr))+'\n防伪码文件存放位置'+datafile)
        root.withdraw()








