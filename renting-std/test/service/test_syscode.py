# -*- coding: utf-8 -*-

import unittest

from app.config import *
from app.service.syscode import *


class SysCodeTestCase(unittest.TestCase):
    def test_get_code(self):
        type_name = '户型结构'
        ret = get_code(CODE_TS[type_name])
        print(ret)
        print(ret.values())
        print(ret.keys())

    def test_get_code_4(self):
        dt = get_code(4)
        ca = '{}|{}'.format('安庆市', '枞阳县')
        dt_v = None
        if dt and ca in dt.keys():
            dt_v = dt[ca]
        if dt_v:
            sp = dt_v.split(':')
            sp2 = sp[1].split('|')
            city = sp2[0]
            area = '{}:{}'.format(sp2[1], sp[0])
            print('city: {}, area: {}'.format(city, area))
