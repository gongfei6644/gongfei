# -*- coding: utf-8 -*-
# @Time    : 2019-04-18 12:25
# @Author  : luomingming
# @Desc    :


import unittest
from datetime import datetime
import random
from FxtDataAcquisition.utils import functions
from FxtDataAcquisition.utils.dbs.pymongo_manager import factory

clt = factory.collection('uuid_test')


class FunctionsTestCase(unittest.TestCase):
    def test_uuid(self):
        crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        crt_time = crt_time[0:7].replace('-', '')
        detail_link = 'http://bj.fangtan007.com/sale/detail/{}'
        unit_price = '{}'
        for i in range(0, 10000000):
            uid = functions.uuid([
                detail_link.format(random.randint(100000, 999999)),
                unit_price.format(random.uniform(10000, 99999)),
                crt_time])
            print(uid)
            clt.insert_one({'_id': uid})

    def test_get_uuid(self):
        lst = clt.find().limit(4000)
        for uid in lst:
            print(uid['_id'])

    def test_update_uuid(self):
        lst = clt.find()
        for uid in lst:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            clt.update_one({'_id': uid['_id']}, {'$set': {'update': now}})

    def test_del_uuid(self):
        lst = clt.find().skip(100).limit(1000)
        for uid in lst:
            clt.delete_one({'_id': uid['_id']})

    def test_to_str(self):
        print(functions.to_str(None))
        print(functions.to_str([1, ' 2']))
        print(functions.to_str((1, ' 2')))
        print(functions.to_str('  133 '))
        print(functions.to_str({'name': '赵云'}))
