import csv

# 单条数据写入writerow
with open('test.csv','w') as f:
    # 初始化写入对象
    writer = csv.writer(f)
    # 写入数据
    writer.writerow(['大旭','36'])
    writer.writerow(['超哥哥','25'])

# 多条数据写入(writerows())
with open('test.csv','w') as f:
    writer = csv.writer(f)
    # 注意参数 ： [(),(),()]
    writer.writerows([('大旭','36'),('小泽','34')])













