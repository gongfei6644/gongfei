# -*- coding: utf-8 -*-
# @Desc    : 重置标准化状态数据为最初未标准化状态


import os
import sys

current = os.path.abspath(__file__)
prj_path = os.path.dirname(os.path.dirname(current))
sys.path.append(prj_path)


import re
from app.dbs.pymongo_manager import factory
from app.switch_table import *


def reset():
    base_table = 'renting_case'
    base_table2 = 'renting_std_case'
    for i in range(0, SPLIT_TABLE_NUM):
        tn = table_name(base_table, i)
        tn2 = table_name(base_table2, i)
        print("table: {}".format(tn))
        clt = factory.collection(tn)
        clt2 = factory.collection(tn2)
        times = 0
        while True:
            # lst = list(clt.find({'city': {'$ne': None}, 'd_status': 1, 'is_std': {'$in': [1, -1]},
            #                      'case_happen_date': {'$gte': '2019-07-20'}}, {'_id': 1}).limit(10000))
            lst = list(clt.find({'city': {'$ne': None}, 'd_status': 1, 'is_std': {'$in': [1, -1]},
                                 'case_happen_date': {'$gte': '2019-07-20'}, 'project_name': {
                    '$in': [re.compile('\d+栋.*'), re.compile('\d+单元.*'), re.compile('\('), re.compile('（')]}}
                                , {'_id': 1}).limit(10000))
            if not lst:
                lst = list(clt.find({'city': {'$ne': None}, 'd_status': 1, 'is_std': {'$in': [1, -1]},
                                     'case_happen_date': {'$gte': '2019-07-20'}, 'project_name': {
                        '$in': [re.compile('旁'), re.compile('旁边'), re.compile('对面'), re.compile('后面'),
                                re.compile('附近'), re.compile('车库'), re.compile('商铺'), re.compile('厂房库房'),
                                re.compile('店面'), re.compile('门面'), re.compile('写字楼'), re.compile('铺面')]}}
                                    , {'_id': 1}).limit(10000))
            if not lst:
                break
            ids = []
            for id in lst:
                ids.append(id['_id'])
            r = clt.update_many({'_id': {'$in': ids}}, {"$set": {"is_std": 0}}, upsert=False)

            r2 = clt2.delete_many({'case_id': {'$in': ids}})
            times = times + 1
        print('times: ' + str(times))


def reset2():
    base_table = 'renting_case'
    base_table2 = 'renting_std_case'
    for i in range(0, SPLIT_TABLE_NUM):
        tn = table_name(base_table, i)
        tn2 = table_name(base_table2, i)
        print("table: {}、{}".format(tn,tn2))
        clt = factory.collection(tn)
        clt2 = factory.collection(tn2)

        r = clt.update_many({'city': {'$ne': None}, 'd_status': 1, 'is_std': {'$in': [1, -1]},
                             'detail_time': {'$gte': '2019-01-01'}}, {"$set": {"is_std": 0}}, upsert=False)
        r2 = clt2.delete_many({'case_happen_date': {'$gte': '2017-01-01'}})

    print('完成')


if __name__ == '__main__':
    reset2()
    pass
