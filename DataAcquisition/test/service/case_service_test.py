# -*- coding: utf-8 -*-
# @Time    : 2019-05-08 18:16
# @Author  : luomingming
# @Desc    :

import unittest

from pypinyin import lazy_pinyin

from FxtDataAcquisition.repository.case_repo import CaseRepo
from FxtDataAcquisition.service.case_service import CaseService
from FxtDataAcquisition.settings import *


class CaseRepoTestCase(unittest.TestCase):
    def setUp(self):
        self.case_service = CaseService(CaseRepo())

    def test_get_raw_case(self):
        lst = self.case_service.get_raw_case(SITE_FANGTAN)
        print(lst)

    def test_choice_cities(self):
        for i in range(1, 1000):
            print(self.case_service.choice_cities(
                SITE_FANGTAN, ''.join(str(i) for i in lazy_pinyin(SITE_FANGTAN))))
