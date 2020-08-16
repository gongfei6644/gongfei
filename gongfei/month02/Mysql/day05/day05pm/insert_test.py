# insert_test.py
# 插入示例
import pymysql
from db_conf import *
conn = pymysql.connect(
    host, user, passwd, dbname) # 连接数据库
cursor = conn.cursor()  # 获取游标
# 执行SQL
# sql = """
# insert into orders(order_id,cust_id)
# values('201801010007','C00000007')
# """
sql = """delete from orders 
where order_id='201801010007' """#删除
cursor.execute(sql) #执行插入
conn.commit()       #提交事务
print("执行成功")
cursor.close()      #关闭游标
conn.close()        #关闭数据库连接
