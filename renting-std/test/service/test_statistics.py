# -*- coding: utf-8 -*-


import unittest

from app.service.statistics import *


class StatisticsTestCase(unittest.TestCase):

    def test_statis_to_mysql(self):
        statis_to_mysql()

    def test_get_statis(self):
        get_statis('广州', '房天下二手房', '2018-10-07')
