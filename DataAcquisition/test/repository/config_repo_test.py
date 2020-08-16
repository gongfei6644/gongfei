# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 11:53
# @Author  : luomingming
# @Desc    :


import unittest

from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.settings import *


class ConfigRepoTestCase(unittest.TestCase):
    def setUp(self):
        self.config_repo = ConfigRepo()

    def test_get_all_urls(self):
        lst = self.config_repo.get_all_urls(SITE_FANGTAN)
        print(lst)

    def test_get_detail(self):
        detail = self.config_repo.get_detail('http://bj.fangtan007.com/sale/r110227-b313/')
        print(detail)

    def test_delete(self):
        ret = self.config_repo.delete(SITE_FANGTAN, '重庆')
        print(ret)

    def test_get_cities(self):
        ret = self.config_repo.get_cities(SITE_FANGTAN)
        for city in ret:
            print(city)
