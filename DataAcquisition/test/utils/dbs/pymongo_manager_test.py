# -*- coding: utf-8 -*-
# @Time    : 2019-05-06 14:25
# @Author  : luomingming
# @Desc    :

import unittest
from FxtDataAcquisition.utils.dbs.pymongo_manager import factory

clt = factory.collection('Dat_case')


class PymongoManagerTestCase(unittest.TestCase):
    def test_update_status(self):
        clt.update_many({'d_status': 2}, {'$set': {'d_status': None}})
