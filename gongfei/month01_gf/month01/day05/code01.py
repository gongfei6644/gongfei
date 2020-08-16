"""
    list 列表常用操作
"""

# str01 = "abcd"
# # 由于字符串是不可变的，所谓修改只是创建新的
# str02 = str01.replace("a","A")
# print(str01,str02 )

# 1. 创建空列表
list01 = []
list01 = list()

# 创建具有元素的列表
list02 = ["a", 1, True]
# 存放可迭代对象
list02 = list(range(3))

# 2. 增加
# 在末尾追加
list01.append("A")
list01.append("B")
# 插入
list01.insert(1,"QTX")
print(list01,list02)

# 3, 删除
# 删除指定元素
list01.remove("B")
# 删除指定索引的元素
del list01[0]
print(list01)

# 4. 修改
list01[0] = "qtx"
# list01[1] = "qtx"  # 索引越界
print(list01)
# 通过切片改变元素
list02[0:2] = ["a","b"]
print(list02)
list02[0:0] = ["A","B"]
print(list02)

# 5. 正向获取所有元素
for item in list02:
    print(item)

# 反向获取所有元素
# for 使用的是索引
for i in range(len(list02)-1,-1,-2):
    print(list02[i])














