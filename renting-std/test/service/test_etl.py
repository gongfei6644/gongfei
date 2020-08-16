# -*- coding: utf-8 -*-


import unittest

from bson.objectid import ObjectId


class ETLTestCase(unittest.TestCase):

    def test_mongo_id(self):
        id = ObjectId("5349b4ddd2781d08c09890f3")
        print(str(id))
