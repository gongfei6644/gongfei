# -*- coding: utf-8 -*-


import random
import threading
import unittest
from hashlib import md5

from app.dbs.pymongo_manager import factory
from app.models.std_case import StdCase


class StdCaseTestCase(unittest.TestCase):

    def test_select_distinct(self):
        ret = StdCase().select_distinct()
        for case in ret:
            print(case)

    def test_md5(self):
        t = md5("test".encode('utf-8'))
        print(t.hexdigest())

    def test_del_dups(self):
        StdCase().del_dups()

    def test_get_dups(self):
        ret = StdCase().get_dups('北京市', '2019-01-10 00:00:00',
                                 '2019-05-16 23:59:59')._CommandCursor__data
        if not ret:
            print('None')
        for case in ret:
            print(case)

    def test_get_by_usage(self):
        StdCase().get_by_type('usage', '北京市', '2019-01-10 00:00:00', '2019-05-16 23:59:59')

    def test_get_by_btype(self):
        StdCase().get_by_type('btype', '北京市', '2019-01-10 00:00:00', '2019-05-16 23:59:59')

    def test_get_by_project(self):
        StdCase().get_by_type('project', 0.5, '北京市', '2019-01-10 00:00:00', '2019-05-16 23:59:59')

    def test_select_nomal_data(self):
        ret = StdCase().get_list('北京市', '2019-01-10', '2019-05-16', page_index=1, status=[1])
        if not ret:
            print('None')
        for case in ret:
            print(case.case_happen_date)

    def test_reset_status(self):
        collection = factory.collection('std_case')
        rs = collection.update_many({'status': 0}, {'$set': {'status': 1}})
        print(rs)

    def test_update_status(self):
        ret = StdCase().update_status(' 2019-06-01 00:00:00 ', ' 2019-06-05 23:59:59 ')
        print(ret)

    # 删除字段
    def test_reset_case(self):
        collection = factory.collection('std_case')
        rs = collection.update({"status": {"$exists": True}}, {"$unset": {"status": ""}}, multi=True, upsert=False)
        print(rs)

    def test_date_to_str(self):
        threading.Thread(target=self.date_to_str).start()
        threading.Thread(target=self.date_to_str).start()
        threading.Thread(target=self.date_to_str).start()
        threading.Thread(target=self.date_to_str).start()
        threading.Thread(target=self.date_to_str).start()
        print('--------')

    def date_to_str(self):
        collection = factory.collection('std_case')
        idx = 0
        while True:
            lst = list(collection.find({'case_happen_date': {'$type': 'date'}})
                       .skip(random.randint(0, 10000)).limit(1000))
            if not lst:
                lst = list(collection.find({'case_happen_date': {'$type': 'date'}}).limit(1000))
            if not lst:
                idx += 1
                if idx > 100:
                    break
            for case in lst:
                dt = case['case_happen_date']
                dt = dt.strftime('%Y-%m-%d')
                ret = collection.update({'_id': case['_id']}, {'$set': {'case_happen_date': dt}})
                print(ret)

    def test_get_by_ids(self):
        lst = StdCase().get_by_case_ids(['af061e42f01f97cc56dc8305bda375aa'])
        print(lst)
