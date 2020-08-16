# -*- coding: utf-8 -*-
# @Time    : 2019-04-18 11:30
# @Author  : luomingming
# @Desc    :


import unittest
import re


class RegexTestCase(unittest.TestCase):
    def test_unitprice(self):
        price = '80282元/㎡'
        m = re.match('\d+', price)
        if m:
            print(m.group())

    def test_floor_split(self):
        v = '9/16 F'
        m = re.findall('\d+', v)
        print(m)

    def test_page(self):
        url = 'http://gz.fangtan007.com/sale/r440105-b63-p3/'
        url = 'http://nj.sell.house365.com/district/dl_p11.html'
        url = 'http://hz.sell.house365.com/district_d5/dl_p6.html'

        url = url.rstrip('/')
        url = url[url.rindex('/'):]
        target = re.findall('p[0-9]+', url)
        print(int(target[0][1:]))
