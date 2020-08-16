# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 11:53
# @Author  : luomingming
# @Desc    :


import unittest

from pymongo import InsertOne

from FxtDataAcquisition.repository.case_repo import CaseRepo
from FxtDataAcquisition.settings import *


class CaseRepoTestCase(unittest.TestCase):
    def setUp(self):
        self.case_repo = CaseRepo()

    def test_find(self):
        lst = self.case_repo.find(SITE_FANGTAN, ['北京市', '上海市'])
        for case in lst:
            print(case)

    def test_exist(self):
        exist = self.case_repo.exist(SITE_FANGTAN, '深圳市')
        print(exist)

    def test_batch_update(self):
        try:
            lst = [InsertOne(
                {'list_page_url': 'http://gz.fangtan007.com/sale/r440111-b84/', 'case_happen_date': '2019-04-23',
                 'data_source': '房探网', 'city': '广州', 'area': '白云', 'sub_area': '黄石',
                 'title': '富力阳光美居高层复式，豪华装修，有天台花园，业主换别墅。', '_id': '6bf77b4037e62a914c57e37dcc089569',
                 'unitprice': '30898', 'source_link': 'http://gz.fangtan007.com/sale/detail/1322959',
                 'crt_time': '2019-04-25 11:48:11', 'project_name': '富力阳光美居', 'house_area': '167'}), InsertOne(
                {'list_page_url': 'http://gz.fangtan007.com/sale/r440111-b84/', 'case_happen_date': '2019-04-19',
                 'data_source': '房探网', 'city': '广州', 'area': '白云', 'sub_area': '黄石',
                 'title': '【真实房】富力阳光美居南北对流接地气，精装两房，安静，望花园', '_id': '18b1aa462be2e1e47da35f2e8aeff8be',
                 'unitprice': '31429', 'source_link': 'http://gz.fangtan007.com/sale/detail/1323202',
                 'crt_time': '2019-04-25 11:48:59', 'project_name': '富力阳光美居', 'house_area': '63'})]
            self.case_repo.batch_update(lst)
        except Exception as e:
            print(e)

    def test_update_status(self):
        self.case_repo.update_status(None, -1, '西安市', 'http://xa.fangtan007.com/sale/detail/316628')
