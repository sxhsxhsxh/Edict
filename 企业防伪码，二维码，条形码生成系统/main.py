from menu import *
import os,time,string,random,tkinter,qrcode
from pystrich.ean13 import EAN13Encoder
from tkinter import *
from string import digits
from hanshu import *
from tkinter import filedialog
import qrcode


#建立根窗口
root = tkinter.Tk()


def scode1(cmd):
    '''生成6位数据防伪码'''
    count = input_box('请输入您要生成的防伪码的数量',1,0)
    while count == 0:
        print('您输入的数量不对，请重新输入')
        count = input_box('请输入您要生成的防伪码的数量', 1, 0)
    randstr.clear()
    for j in range(int(count)):
        randfir = ''
        for i in range(6):
            randfir += random.choice(number)
        randfir += '\n'
        randstr.append(randfir)
    wfile(randstr,'scode'+cmd+'.txt','','已生成6位防伪码,共计:','codepath')

def scode2(cmd):
    '''生成系列产品的数字编码'''
    start_count = input_box('请输入输入系列产品的起始号',3,3)
    while start_count == 0:
        start_count = input_box('请输入系列产品的起始号',3,3)
    ord_count =  input_box('请输入系列产品的数量',1,0)
    while int(ord_count)<1 or int(ord_count)>9999:
        #当数量大于9999或者小于1时，重新输入
        ord_count = input_box('请输入系列产品的数量', 1, 0)
    incount = input_box('请输入每个系列产品的防伪码数量',1,0)
    while int(incount) == 0:
        incount = input_box('请输入你要生成的防伪码数量',1,0)
    randstr.clear()
    for m in range(int(ord_count)): #分类产品编号
        for j in range(int(incount)): #产品防伪码编号
            randfir = ''
            for i in range(6):   #生成不含类别的产品防伪码
                randfir +=random.choice(number)#每次生成一个随机因子
            #将生成的单条防伪码添加到防伪码列表
            randstr.append(str(start_count)+randfir+'\n')
    wfile(randstr,'scode'+cmd+'.txt','','已生成9位系列产品防伪码,共计：','codepath')

def scode3(cmd):
    '''生成25位混合产品序列号'''
    incount = input_box('请输入要生成的25位混合产品序列号的数量',1,0)
    while incount == 0:
        print('您输入的数量不对，请重新输入')
        incount = input_box('请输入您要生成的防伪码的数量', 1, 0)
    randstr.clear()
    for j in range(int(incount)):
        strone = '' #保存生成的单条防伪码
        for i in range(25):
            strone += random.choice(letter)
            #每隔５位加上一条横线
        strtow = strone[:5]+'-'+strone[5:10]+'-'+strone[10:15]+'-'+strone[15:20]+'-'+strone[20:25]+'\n'
        randstr.append(strtow)
    wfile(randstr,'scode'+cmd+'.txt','','已生成25位防伪码,共计:','codepath')

def scode4(cmd):
    '''生成含数据分析功能的防伪编码'''
    intype = input_box('请输入数据分析编号',2,3)
    while not str.isalpha(intype) or len(intype) != 3:
        #判断输入的类型是否是字符类型和输入的内容长度是是否为３
        intype = input_box('请输入数据分析编号', 2, 3)
    incount = input_box('输入防伪码的数量',1,0)
    while int(incount) == 0:
        #判断输入的数字是否大于０
        incount = input_box('请输入数据分析编号', 2, 3)
    ffcode(incount,intype,'',cmd)

def ffcode(scount,typestr,ismessage,cmd):
    randstr.clear()
    for j in range(int(scount)):
        strpro = typestr[0].upper()#取出第一个字母转换成大写
        strtype = typestr[1].upper() #取出第二个字母，转换成大写
        strclass = typestr[2].upper()#取出第三个字母，转换成大写
        randfir = random.sample(number,3)
        randsec = sorted(randfir)#对抽取的位置进行排序
        letterone = ''
        for i in range(9): #生成9位数字防伪码
            letterone += random.choice(number)
        sim = str(letterone[0:int(randsec[0])]) + strpro + str(
            letterone[int(randsec[0]):int(randsec[0])]) + strtype + str(
            letterone[int(randsec[1]):int(randsec[2])]) + strclass + str(letterone[int(randsec[2]):9]) + '\n'
        randstr.append(sim)
    wfile(randstr,typestr+'scode'+cmd+'.txt',ismessage,'生成含数据分析功能的防伪码','codepath')

def scode5(cmd):
    default_dir = r'codeauto.mri'
    #打开文件选择对话框,指定打开的文件名称为＇codeauyo.aut,可以使用记事本打开和编辑＇
    file_path = tkinter.filedialog.askopenfilename(filetypes=[('Text File','*.mri')],
        title = u'请选择智能批处理文件：',initialdir=(os.path.expanduser(default_dir)))
    codelist = openfile(file_path) #读取文件
    codelist = codelist.split('\n')
    print(codelist)
    for item in codelist:
        print(item)
        codea = item.split(',')[0]
        codeb = item.split(',')[1]
        ffcode(codeb,codea,'no',cmd)

def scode6(cmd):
    '''条形码批量生成'''
    mainid = input_box('请输入国家代码(3位):',1,0)
    while int(mainid) < 1 or len(mainid)>3:
        '''当输入的国家代码小于1整数或者长度小于3时，重新输入'''
        mainid = input_box('请输入国家代码:', 1, 0)
    compid = input_box('请输入企业代码(４位):',1,0)
    while int(compid) < 1 or len(compid) > 4:
        '''当输入的企业代码小于1整数或者长度小于4时，重新输入'''
        compid = input_box('请输入企业代码(４位):', 1, 0)
    incount = input_box('请输入要生成条形码的数量:',1,0)
    while int(incount) == 0:
        '''输入生成条形码的数量为0时，重新输入'''
        incount = input_box('请输入要生成条形码的数量:', 1, 0)
    mkdir('barcode') #判断条形码的文件夹是否存在，如果不存在，则创建
    for j in range(int(incount)):
        strone = ''
        for i in range(5):
            strone += str(random.choice(number))
        barcode = mainid + compid + strone #把国家代码，机器码，随机生成的代码进行组合
        #极端条形码的校检位
        evensum = int(barcode[1])+int(barcode[3])+int(barcode[5])+int(barcode[7])+int(barcode[9]) +int(barcode[11])
        oddsm = int(barcode[2])+int(barcode[4])+int(barcode[6])+int(barcode[8])+int(barcode[10])
    checkbit = int(10-((evensum*3 + oddsm)%10)%10)
    barcode += str(checkbit)#组成完整的13位条形码
    encoder = EAN13Encoder(barcode) #调用EAN13模块生成条形码
    encoder.save('barcode\\'+barcode+'.png')

def scode7(cmd):
    incount = input_box('请输入要生成12位数字的二维码数量:',1,0)
    while int(incount) == 0:
        '''输入数量为0时,重新输入'''
        incount = input_box('请输入要生成12位数字的二维码数量:', 1, 0)
    mkdir('qrcode')
    for j in range(int(incount)):
        strone = ''
        for i in range(12):
            strone += str(random.choice(number))
        encoder = qrcode.make(strone)
        encoder.save('qrcode\\'+strone+'.png')



def main():
    while True:
        menu()
        cmd = input("请输入命令:")
        if cmd not in ['1','2','3','4','5','6','7','8'] or not cmd:
            print("输入命令错误,请重新输入")
        else:
            if cmd == "1":
                scode1(cmd)
            elif cmd == "2":
                scode2(cmd)
            elif cmd == "3":
                scode3(cmd)
            elif cmd == "4":
                scode4(cmd)
            elif cmd == "5":
                scode5(cmd)
            elif cmd == "6":
                scode6(cmd)
            elif cmd == "7":
                scode7(cmd)
            elif cmd == "8":
                data = input("是否退出系统，Y/N")
                if data == 'Y':
                    print("退出系统")
                    return
                elif data == 'N':
                    continue


if __name__ == "__main__":
    main()
















