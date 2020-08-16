# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 11:53
# @Author  : luomingming
# @Desc    :


import unittest

from FxtDataAcquisition.repository.project_info_repo import ProjectInfoRepo
from FxtDataAcquisition.settings import *


class ProjectInfoRepoTestCase(unittest.TestCase):
    def setUp(self):
        self.case_repo = ProjectInfoRepo()

    def test_find_all(self):
        lst = self.case_repo.find_all(
            start_date='2019-06-01 00:00:00',
            end_date='2019-06-05 23:59:59'
            , cities=['南京市']
            , source=SITE_58_COMMUNITY
        )
        for case in lst:
            print(case)
