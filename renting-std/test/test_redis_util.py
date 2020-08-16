# -*- coding: utf-8 -*-

import unittest

from app.redis_util import *


class RedisUtilTestCase(unittest.TestCase):
    def setUp(self):
        self.conn = conn

    def test_set(self):
        self.conn.set('test', 123456)

        print(self.conn.get('test'))

    def test_exists(self):
        ret = self.conn.keys('city_*')
        print(ret)

    def test_get(self):
        ret = self.conn.smembers('city_天京市')
        print(ret)
