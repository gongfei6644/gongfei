import datetime as dt
from pymongo import MongoClient
from pymongo import InsertOne
from setting import config


class MongoOption(object):

    # 初始化mongo数据库的连接
    def __init__(self, db='DataCollecting'):
        while True:
            try:
                self.client = MongoClient(config.MONGO_URI)
            except:
                pass
            else:
                break
        self.client.options.connectionsPerHost = 20
        self.db = self.client[db]

    def m_select(self, exception={}, collection="Dat_case"):
        """
        查找
        :param exception: 查找语句
        :param collection: 表名, 默认使用
        :return: 查询结果
        """

        self.collection = self.db[collection]
        items = self.collection.find(exception)
        return items

    def m_insert(self, condition, collection="Dat_case"):
        """
        批量插入
        :param condition: InsertOne对象的列表
        :param collection: 表名
        :return: 插入结果
        """
        self.collection = self.db[collection]
        self.collection.bulk_write(condition, ordered=False)

    def s_update(self, exception, dic_data, collection="Dat_case"):
        """
        单个更新
        :param exception: 查找语句
        :param dic_data:  UpdateOne实列
        :param collection: 表名
        :return:
        """
        self.collection = self.db[collection]
        self.collection.update_one(exception, {"$set": dic_data}, upsert=True)

    def m_update(self, condition, collection="Dat_case"):
        """
        批量更新
        :param condition: UpdateOne的实例列表
        :param collection: 表名
        :return:
        """
        try:
            self.collection = self.db[collection]
            self.collection.bulk_write(condition, ordered=False)
        except Exception as e:
            print(e)
            self.collection.bulk_write(condition, ordered=False)

    def get_config(self, city_name, source):
        '''
        获取配置信息
        :param city_name:城市名称
        :return:查询城市下的所有片区信息
        '''
        conllection_config = self.db["config"]
        city_info = list(conllection_config.find({"city": city_name, "source": source}))
        return city_info
