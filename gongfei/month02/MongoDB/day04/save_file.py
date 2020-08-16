from pymongo import MongoClient
import bson.binary

conn = MongoClient('localhost', 27017)
db = conn.images
myset = db.girl
# 　存储图片
# with open('./test.jpg', 'rb') as f:
#     data = f.read()
#
# # 将ｄａｔａ转换为ｂｓｏｎ格式
# content = bson.binary.Binary(data)
#
# # 　插入到集合
# dic = {'filename': 'girl.jpg', 'data': content}
# myset.insert_one(dic)

#　提取文件
img = myset.find_one({'filename':'girl.jpg'})
# print(img)

with open('mm.jpg','wb') as f:
    f.write(img['data'])

conn.close()
