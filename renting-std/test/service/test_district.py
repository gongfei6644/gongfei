# -*- coding: utf-8 -*-

import unittest

from app.service.distinct import *


class DistrictTestCase(unittest.TestCase):
    def test_city(self):
        city('深圳')

    def test_area(self):
        ret = area(75, '江东')
        print(ret)

    def test_cities(self):
        cities()

    def test_areas(self):
        areas()
