# -*- coding: utf-8 -*-


import unittest
from datetime import datetime
from datetime import time
from datetime import timedelta


class DateTimeTestCase(unittest.TestCase):
    def test_01(self):
        print("time: {}, {}".format(datetime.today(), datetime.today()))
        print(datetime.combine(datetime.now(), time.min).strftime('%Y-%m-%d %H:%M:%S'))
        print(datetime.combine(datetime.now(), time.max).strftime('%Y-%m-%d %H:%M:%S'))
        print(datetime.now().strftime('%Y-%m-%d-%H-%M'))

    def test_02(self):
        d = datetime.now().strftime('%Y-%m')
        print(d)
        now = datetime.now()
        d = datetime(int(now.year), int(now.month), 1)
        print(d)

    def test_03(self):
        now = datetime.now()
        d = datetime(int(now.year), int(now.month), int(now.day) - 1).strftime('%Y-%m-%d')
        print(d)

    def test_04(self):
        d = datetime.strptime('2019-01-19', '%Y-%m-%d')
        print(d)

    def test_05(self):
        d = datetime.strptime('2019-01-01', '%Y-%m-%d')
        # d2 = datetime(int(d.year), int(d.month), int(d.day) - 1)
        d2 = d - timedelta(days=1)
        print(d2)
