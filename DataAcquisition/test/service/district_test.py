# -*- coding: utf-8 -*-
# @Time    : 2018-12-20 13:38
# @Author  : luomingming

import unittest
from pypinyin import lazy_pinyin
from FxtDataAcquisition.service import distinct
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.settings import *


class DistrictTestCase(unittest.TestCase):
    def setUp(self):
        self.config_repo = ConfigRepo()

    def test_city(self):
        print(distinct.city('深圳'))
        print(distinct.city('深圳市'))

    def test_cities(self):
        lst = distinct.cities()
        for city in lst:
            print(city)

    def test_get_all_city_name(self):
        cities = self.config_repo.get_cities(SITE_FANGTAN)
        cities = "'" + "','".join(cities) + "'"
        cws = distinct.get_city_weights(cities, ''.join(str(i) for i in lazy_pinyin(SITE_FANGTAN)))
        sp = cws.split(":")
        cities = sp[0].split(',')
        weights = sp[1].split(',')
        ws = []
        for w in weights:
            ws.append(int(w))
        print('cities: {}, weights: {}'.format(cities, ws))

