# order_manage.py
# 订单管理类
from order import *
from order_dao import *

class OrderManage:
    def __init__(self):
        self.order_dao = OrderDao()   #持有数据访问对象

    #根据订单号查询订单
    def query_by_id(self, order_id): 
        if not order_id:
            print("订单编号对象非法")
            return None
        if order_id == "":
            print("订单编号不能为空")
            return None

        return self.order_dao.query_by_id(order_id)

    # 查询所有订单
    def query_all_order(self):
        return self.order_dao.query_all_order()

    # 新增订单
    def insert_order(self, order): 
        if (not order.order_id) or order.order_id == "":
            print("订单编号不能为空")
            return

        if (not order.cust_id) or order.cust_id == "":
            print("客户编号不能为空")
            return

        if order.products_num < 1:
            print("商品数量非法")
            return

        if order.amt - 10.00 < 0.00001:  # 订单金额小于10元
            print("订单金额小于最低起购额度")
            return

        return self.order_dao.insert_order(order)

    # 修改订单
    def update_order(self, order):
        if (not order.order_id) or order.order_id == "":
            print("订单编号不能为空")
            return

        if order.products_num < 1:
            print("商品数量非法")
            return

        if order.amt - 10.00 < 0.00001:  # 订单金额小于10元
            print("订单金额小于最低起购额度")
            return

        return self.order_dao.update_order(order)


