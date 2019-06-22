'''
主函数模块:
    调用menu()函数生成功能选择菜单；
    调用子函数对学生信息的增删改查，统计和排序等功能的实现
'''
from menu import menu
from models import *

def main():
    while True:
        menu()
        cmd = input("请输入命令：")
        if cmd not in ['1','2','3','4','5','6','7','8']:
            print("命令错误，请重新输入")
        elif cmd == '1':
            insert_stu()
        elif cmd == '2':
            find_stu()
        elif cmd == '3':
            delete_stu()
        elif cmd == '4':
            update_stu()
        elif cmd == '5':
            total_stu()
        elif cmd == '6':
            order_by_stu()
        elif cmd == '7':
            find_all_stu()
        elif cmd == '8':
            print("退出系统")
            return


if __name__ == "__main__":
    main()