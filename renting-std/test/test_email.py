# -*- coding: utf-8 -*-

import unittest

from app import email


class EmailTestCase(unittest.TestCase):
    def test_email(self):
        email.send('test', '测试')
