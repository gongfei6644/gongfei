# -*- coding: utf-8 -*-
# @Time    : 2019-04-18 12:25
# @Author  : luomingming
# @Desc    : 测试在mongodb插入数据同时修改表名是否会出现异常


import unittest
from datetime import datetime

import pymongo

from FxtDataAcquisition.utils import functions
from FxtDataAcquisition.utils.dbs.pymongo_manager import factory

clt = factory.collection('rename_test')


class RenameTableWithRunningTestCase(unittest.TestCase):
    def test_insert(self):
        for i in range(0, 10000000):
            uid = functions.uuid([i, 'w'])
            clt.insert_one({'uid': uid, 'name': '芒果灌灌灌灌灌灌灌灌灌灌灌灌笑嘻嘻谢谢',
                            'desc': '在嗡嗡嗡嗡嗡嗡嗡嗡嗡嗡嗡嗡嗡嗡嗡嗡嗡嗡'})

    def test_update(self):
        lst = list(clt.find({}).limit(1000000))
        for coll in lst:
            r = clt.update_one({'_id': coll['_id']}, {'$set': {'name': 'python'}})
            print(r)

    def test_rename(self):
        clt.rename('rename_test_' + datetime.now().strftime('%Y_%m'))
        clt.create_index([('uid', pymongo.ASCENDING)], unique=True, background=True)

    def test_insert_one(self):
        clt.insert_one({'uid': 'bf62e32cb3b29411cefd5d32858d815e'})
