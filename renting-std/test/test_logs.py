# -*- coding: utf-8 -*-

import unittest

from app import logs


class LogsTestCase(unittest.TestCase):
    def test_log(self):
        log = logs.log(__name__, 'test')
        log.debug('test---------------')
