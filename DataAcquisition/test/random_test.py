# -*- coding: utf-8 -*-
# @Time    : 2019-05-08 14:36
# @Author  : luomingming
# @Desc    :

import unittest
import random


class RandomTestCase(unittest.TestCase):
    def test_random_weight(self):
        cities = ['北京市', '上海市', '长沙市', '重庆市', '衡阳市']
        weights = [9, 9, 4, 5, 2]   # 跟城市列表一一对应
        bj = 0
        sh = 0
        cs = 0
        cq = 0
        hy = 0
        for i in range(1, 1000):
            city = random.choices(cities, weights)[0]
            # print(city)
            if city == '北京市':
                bj += 1
            elif city == '上海市':
                sh += 1
            elif city == '长沙市':
                cs += 1
            elif city == '重庆市':
                cq += 1
            elif city == '衡阳市':
                hy += 1
        print('北京市: {}, 上海市: {}, 长沙市: {}, 重庆市: {}, 衡阳市: {}'.format(bj, sh, cs, cq, hy))

    def test_random_int(self):
        proxy = [0, 1]
        weights = [4, 6]
        for i in range(0, 10):
            print(random.choices(proxy, weights)[0])
            # print(random.randint(1, 2))
