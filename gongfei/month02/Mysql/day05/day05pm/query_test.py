# query_test.py
# pymysql查询示例
# 导入PyMySQL模块
import pymysql
from db_conf import *
# 建立数据库连接
#调用pymysql模块下connect函数连接数据库
#连接成功后，返回一个连接对象，放到conn变量中
conn = pymysql.connect(
    host, user, passwd, dbname)
cursor = conn.cursor() # 创建游标对象
# 使用游标对象提供的方法，执行SQL语句
sql = "select * from orders"
cursor.execute(sql)  #执行SQL语句
result = cursor.fetchall() #取出所有数据
for row in result:  #循环取出每行数据并打印
    order_id = row[0] #订单编号
    cust_id = row[1]  #客户编号
    amt = row[5]      #金额
    print("编号:%s,编号:%s,金额:%s"%
      (order_id,cust_id,amt))
# 关闭游标
cursor.close()
# 关闭数据库
conn.close()
