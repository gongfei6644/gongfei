# order_manage_ui.py
# 订单管理程序ui层
from order import *
from order_manage import *

# 全局变量
om = None

def print_menu(): #打印主菜单
    menu = '''
    --------------- 订单管理程序 ---------------
      1 - 查询所有订单      
      2 - 根据订单号查询
      3 - 新增订单
      4 - 修改订单         
      5 - 删除订单
      其它 - 退出
    '''
    print(menu)  

def query_all():   #查询所有订单
    orders = om.query_all_order()
    for a in orders:
        print(a)

def query_by_id(): #根据订单号查询
    order_no = input("请输入要查询的订单号：")
    if not order_no:
        print("输入订单号不合法")
        return
    
    order = om.query_by_id(order_no)
    print("\n查询结果:")
    print(order)   #打印订单信息
    print("\n")

def add_order(): #新增订单
    try:
        order_no = input("请输入订单号:")
        cust_id = input("请输入客户编号:")
        products_num = int(input("请输入商品数量："))
        amt = float(input("请输入订单金额:"))

        new_order = Order(order_no, cust_id, products_num, amt)
        ret = om.insert_order(new_order)
        print(ret)
    except Exception as e:
        print("操作错误")
        print(e)
    return    

def main(): #主函数
    global om
    om = OrderManage()  #实例化orderManage对象

    while True:
        print_menu()
        oper = input("请选则要执行的操作:")
        if oper == "1":  #查询所有订单
            query_all()
        elif oper == "2":  #根据订单号查询
            query_by_id()
        elif oper == "3":  #新增订单
            add_order()
        elif oper == "4":  #修改订单
            pass
        elif oper == "5":  #删除订单
            pass
        else:
            break

if __name__ == "__main__":
    main()
