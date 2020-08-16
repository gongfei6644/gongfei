import pymongo

database = 'maoyandb'
table = 'filmset'

# 3个对象
conn = pymongo.MongoClient('localhost',27017)
db = conn[database]
myset = db[table]
# 执行插入语句
myset.insert_one({'name':'Tiechui'})
# insert_many(),参数为列表
myset.insert_many(
    [{'name':'周芷若'},{'name':'赵敏'}]
)















