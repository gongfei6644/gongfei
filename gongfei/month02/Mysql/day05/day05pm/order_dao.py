# order_dao.py
# 订单数据访问对象
# d:data a:access o:object
from order import *
from db_helper import *
# 拼装各种SQL语句，调用DBHelper的对象
# 实现数据库的操作
class OrderDao:
    def __init__(self): #构造函数
        #创建、持有DBHelper对象
        self.db_helper = DBHelper()
        self.db_helper.open_conn()#打开连接
    
    #析构函数,对象销毁时调用
    def __del__(self): 
        self.db_helper.close_conn()

    #查询所有订单, 返回订单对象列表
    def query_all_order(self):
        sql = "select * from orders"
        order_list = []  #订单对象列表
        result = self.db_helper.do_query(sql)
        if not result:  #返回空对象
            print("查询结果为空")
            return None #返回空对象
        for row in result: #遍历返回结果集
            order_id = row[0]  #订单编号
            cust_id = row[1]   #客户编号
            if row[4]:   #商品数量
                products_num = int(row[4])
            else:
                products_num = 0
            if row[5]:  #订单金额
                amt = float(row[5])
            else:
                amt = 0.00
            order_list.append(Order(order_id,
                cust_id, products_num, amt))
        return order_list  #返回订单对象列表

# 测试
if __name__ == "__main__":
    orderDao = OrderDao() #实例化数据访问对象
    order_list = orderDao.query_all_order()#查询
    for o in order_list: #遍历订单对象列表
        print(o)
    