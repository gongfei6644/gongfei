# -*- coding: utf-8 -*-

import pprint
import unittest

from app.dbs.pymongo_manager import factory


class MongoManagerTestCase(unittest.TestCase):
    def setUp(self):
        print('启动设置')

    def tearDown(self):
        print('测试结束关闭资源')

    def test_client_pymongo(self):
        collection = factory.collection('Dat_case')
        datas = collection.find()
        pprint.pprint(datas.count())
        num = 0
        for data in datas:
            pprint.pprint(data)
            num = num + 1

        print(num)
