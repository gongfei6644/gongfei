# -*- coding: utf-8 -*-
# @Desc    :

import unittest

from app.switch_table import *
from app.models.case import Case


class SwitchTableTestCase(unittest.TestCase):
    def test_table_idx(self):
        # print(int(md5('南宁市'.encode('UTF-8')).hexdigest(), 16))
        print(table_idx('广州市'))
        print(table_idx('上海市'))
        print(table_idx('北京市'))
        print(table_idx('深圳市'))

    def test_switch(self):
        table = 'Dat_case_01'
        with switch_collection(Case, table):
            Case().save({'tt': 'xx'})
        pass

    def test_range(self):
        # lst = range(0, SPLIT_TABLE_NUM)
        # for i in lst:
        #     print(i)
        lst = range(SPLIT_TABLE_NUM - 1, -1, -1)
        for i in lst:
            print(i)

    def test_random(self):
        for i in range(100):
            print(random.randint(0, 49))

