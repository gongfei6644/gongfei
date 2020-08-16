# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 15:06
# @Author  : luomingming
# @Desc    :

import unittest

from FxtDataAcquisition.utils.mq_client import mq


class RabbitmqClientTestCase(unittest.TestCase):
    def test_conn(self):
        conn = mq.conn()
        channel = conn.channel()
        print(channel)
