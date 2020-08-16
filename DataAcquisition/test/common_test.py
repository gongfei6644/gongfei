# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 16:53
# @Author  : luomingming
# @Desc    :


import unittest
import random
import re
from FxtDataAcquisition.items import CaseItem
from FxtDataAcquisition.spiders import common
from FxtDataAcquisition.settings import *


class CommonTestCase(unittest.TestCase):

    def test_statis(self):
        item = CaseItem()
        item['data_source'] = SITE_FANGTAN
        item['city'] = '重庆'
        for i in range(0, 30):
            if (i % 2) == 0:
                item['project_name'] = None
                item['unitprice'] = None
                item['house_area'] = None
            else:
                item['project_name'] = 'pn{}'.format(i)
                item['unitprice'] = random.choice([8000, 10000])
                item['house_area'] = random.choice([70, 200])
            common.statis(DAQ_LIST, item)
            common.statis(DAQ_DETAIL, item)

    def test_time_sub(self):
        t = '2019-03-04 23:59:59'
        print(t[0:7].replace('-', ''))

    def test_yield(self):
        mylist = [x * x for x in range(3)]
        for i in mylist:
            print(i)
        for i in mylist:
            print(i)
        print('----------------')

        mygenerator = (x * x for x in range(3))
        for i in mygenerator:
            print(i)
        for i in mygenerator:
            print(i)

    def test_regex(self):
        w1 = '中国123'
        w2 = 'hello'
        m1 = re.match('[\u4e00-\u9fa5]', w1)
        m2 = re.match('[\u4e00-\u9fa5]', w2)
        print()

    def test_replace(self):
        s = """房源特点：
                        
                        地标建筑
                        
                    """
        print(s.replace('\s', ''))
        print(re.sub('\s', '', s))

    def test_dict(self):
        finished = {}
        if 'xx' not in finished.keys():
            finished['xx'] = set('a')
        finished.get('xx').add('b')
        finished.get('xx').add('c')
        finished.get('xx').add('c')
        print(finished)
        lst = list(finished.get('xx'))
        print(lst)
