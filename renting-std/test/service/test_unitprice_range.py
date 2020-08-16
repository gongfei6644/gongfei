# -*- coding: utf-8 -*-

# @Desc    :


import unittest

from app.service.unitprice_range import *


class UnitpriceRangeTestCase(unittest.TestCase):
    def test_valid_uprice_r(self):
        try:
            r = valid_uprice_r('百色市', 100)
        except Exception as e:
            print(e.args[0])
        print(r)
