import time
import datetime

from dateutil.relativedelta import relativedelta
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

    def m_select(self, exception={}, collection="renting_case"):
        """
        查找
        :param exception: 查找语句
        :param collection: 表名, 默认使用
        :return: 查询结果
        """

        self.collection = self.db[collection]
        items = self.collection.find(exception)
        return items

    def m_insert(self, condition, collection="renting_case"):
        """
        批量插入
        :param condition: InsertOne对象的列表
        :param collection: 表名
        :return: 插入结果
        """
        self.collection = self.db[collection]
        self.collection.bulk_write(condition, ordered=False)

    def s_insert(self,condition,collection='renting_case'):
        """
        :param condition: InsertOne 对象
        :param collection: 表名
        :return: 插入结果
        """
        try:
            self.collection = self.db[collection]
            result = self.collection.insert_one(condition)
            return result
        except:
            print('插入异常，重复数据')

    def s_update(self, exception, dic_data, collection="renting_case"):
        self.collection = self.db[collection]
        self.collection.update_one(exception, {"$set": dic_data}, upsert=True)

    def m_update(self, condition, collection="renting_case"):
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

    def m_delete(self,condition,collection='renting_case'):
        """
        :param condition: deleteMany 对象
        :param collection: 表名
        :return:
        """
        try:
            self.collection = self.db[collection]
            result = self.collection.remove(condition)
            return result
        except Exception as e:
            print('删除数据异常:',e)

    def statistics(self,exception={},collection='renting_case'):
        """
        统计数量
        :param exception: 查找统计语句
        :param collection: 表名
        :return:
        """
        try:
            self.collection = self.db[collection]
            count = self.collection.find(exception).count()
            return count
        except Exception as e:
            print(e)

    def statistics_aggregate(self,exception={},collection='renting_case'):
        """
        统计数量
        :param exception: 查找统计语句
        :param collection: 表名
        :return:
        """
        try:
            self.collection = self.db[collection]
            result = self.collection.aggregate(exception)
            return result
        except Exception as e:
            print(e)

    def get_config(self, city_name, source):
        '''
        获取配置信息
        :param city_name:城市名称
        :return:查询城市下的所有片区信息
        '''
        conllection_config = self.db["config"]
        city_info = list(conllection_config.find({"city": city_name, "source": source}))
        return city_info
