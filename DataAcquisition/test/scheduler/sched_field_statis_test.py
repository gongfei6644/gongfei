# -*- coding: utf-8 -*-
# @Time    : 19-4-24 下午7:55
# @Author  : luomingming

import unittest
from FxtDataAcquisition.scheduler.sched_field_statis import *


class SchedFieldStatisTestCase(unittest.TestCase):
    def test_send(self):
        send_incr_list()
        send_incr_detail()
        send_list()
        send_detail()
