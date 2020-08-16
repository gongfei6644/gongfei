# order_manage_ui.py
# (UI:User Interface，用户接口)
# 订单管理程序用户接口层(视图层, View)
# 接收用户指令、显示执行结果
from order import *
from order_manage import *

orderManage = None #订单管理对象，全局变量

def print_menu(): #打印主菜单
    menu = '''------ 订单管理程序 ------
    1 - 查询所有订单
    2 - 根据ID号查询订单
    3 - 新增订单
    4 - 修改订单
    5 - 删除订单
    其它 - 退出  '''
    print(menu)

def query_all(): #查询所有订单
    order_list = orderManage.query_all_order()
    for o in order_list:
        print(o)

def　main():
    global orderManage 
    orderManage = OrderManage() #实例化OrderManage
    while True:  #循环打印菜单
        print_menu()
        oper = input("请选择要执行的操作:")
        if oper == "1": #查询所有订单
            query_all()
        elif oper == "2": #根据ID号查询订单 
            pass
        elif oper == "3": #新增订单 
            pass
        elif oper == "4": #修改订单 
            pass
        elif oper == "5": #删除订单 
            pass
        else:  #其它则退出
            break            
if __name__ == "__main__":
    main()
    
