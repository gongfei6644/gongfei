# -*- coding: utf-8 -*-


import unittest

from app.dbs.pymongo_manager import factory
from app.models.case import Case


class CaseTestCase(unittest.TestCase):

    def test_find(self):
        ret = Case().find()
        for case in ret:
            print(case)

    def test_update_std_status(self):
        case = Case()
        case.id = 'e758dfca397c74a882a4387564b7993c'
        case.city = '南京市'
        ret = Case().update_std_status(case, 0)
        print(ret)

    def test_statis(self):
        Case().statis('proj_name_count')

    def test_statis_std(self):
        Case().statis_std()

    # 删除字段
    def test_reset_case(self):
        collection = factory.collection('Dat_case_test')
        rs = collection.update({}, {"$unset": {"is_std": "", "std_date": "", "std_remark": ""}}, multi=True,
                               upsert=False)
        print(rs)

    # 修改字段值（用于测试）
    def test_reset_case(self):
        while True:
            try:
                cases = Case.objects(city__nin=[None, '', '周边', '其它'], d_status=1, is_std__in=[1, -1],
                                     case_happen_date__gte='2019-01-01', data_source='安居客二手房').limit(1000)
                if not cases:
                    break
                for case in cases:
                    r = Case.objects(id=case.id).update_one(set__is_std=0)
                    print(r)
            except Exception as e:
                pass

    def test_update_std(self):
        collection = factory.collection('Dat_case')
        rs = collection.update_many({}, {"$set": {"is_std": 0}}, upsert=False)
        print(rs)

    def test_list_add(self):
        a = [1, 2, 3]
        b = ['a', 'b', 'c']
        c = a + b
        print(c)
