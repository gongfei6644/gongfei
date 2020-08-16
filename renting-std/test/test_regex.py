# -*- coding: utf-8 -*-

import json
import random
import re
import time
import unittest
from datetime import datetime


class RegexTestCase(unittest.TestCase):
    def test_01(self):
        print(re.match('^\\d{1,}$', '11a1'))

    def test_02(self):
        print(re.fullmatch("[\u4E00-\u9FA5]+", '第25层'))
        pattern = re.compile("[\u4E00-\u9FA5]+")
        print(pattern.findall('第25层'))

        # 直接使用match会匹配不到，要是要compile才行
        print(re.match("\\d+[层]$", '第25层'))
        pattern = re.compile("\\d+[层]$")
        print(pattern.search('第25层'))

    def test_03(self):
        print(float(99.44))
        # pattern = re.compile("\\d+[层]")
        pattern = re.compile("\\d+")
        ret = pattern.findall('第25层304号01')
        print(ret[0])
        print(pattern.findall('1214'))

    def test_04(self):
        num = None
        total_floor_num = 1
        if not num and total_floor_num:
            print('yes')

        print('12层'.rstrip('层'))
        pattern = re.compile("[^共]+\\d+[层]")
        ret = pattern.findall('共12层')
        print(ret)

        ret = pattern.findall('1985年建造&#xE147;周层层')
        if ret:
            print()
        print(ret)

    def test_05(self):
        r = '1a'
        try:
            print(int(r))
        except Exception as e:
            print(e)

        r = re.findall('(\d+(\.\d+)?)', '55.95平')
        print(r)
        print(r[0][0])

        for i in range(10):
            print(random.randint(1, 2))
        print(round(10 / 3))

    def test_06(self):
        p = '12（共24层）'
        t1 = '层' in p
        t2 = '共' in p
        if t1 and t2:
            s_str = re.match('(.*?)（共(.*?)）', p)
            print('floor_no:{}, total_floor_num:{}'.format(s_str.group(1), s_str.group(2)))

    def test_07(self):
        word = '两室一厅10'
        for w in word:
            print(w)

    def test_08(self):
        print(re.match('\d{4}', '2018-0223-28 06:03:00.000').group())

        print(re.match('\d{2}(年代)', '80年代'))
        print(re.match('\d{2}(年代)', '80年代').group())

        y = 20
        if y >= 80:
            print('19{}'.format(y + 5))
        elif y == 00:
            print('200{}'.format(y + 5))
        else:
            print('20{}'.format(y + 5))

        t = time.localtime(time.time())
        y = t[0]
        print(y)

    def test_09(self):
        print('西'.split(' '))
        print('西 北'.split(' '))
        print(re.findall('\d+', '10室1厅'))
        print(re.findall('\d+', '10室'))

        print('10室1厅'.index('室'))
        print('10室1厅'[0:3])

    def test_10(self):
        ori = re.sub(r'[^东南西北]', '', '习惯东xxxx南方向西部细胞')
        print(ori)

    def test_11(self):
        r = re.findall('\d+[室厅]', 'xxx33厅d2卫cdaga')
        print('----------------' + r)
        r = re.findall('\d+[室厅]', 'xxx3室3厅xd2卫cdaga')
        r_str = json.dumps(r, ensure_ascii=False)
        if r_str.__contains__('卫'):
            print('卫')
        print(r)
        r = re.findall('\d+[卫]', 'xxx3室3厅xd2卫cdaga')
        print(r)

    def test_12(self):
        ori = re.sub(r'\s', '', '习惯东   xxxx南方向      西部   '
                                '细胞')
        print(ori)

    def test_13(self):
        rt = re.match('^\d{2}[-]\d{2}', '12-28 06:03:00.000')
        if rt:
            yr = rt.group()
            now = datetime.now()
            year = now.year
            nyr = str(year) + '-' + yr
            now_str = now.strftime('%Y-%m-%d')
            if nyr > now_str:
                nyr = str(year - 1) + '-' + yr
            print(nyr)
        # print(re.match('\d{4}[-]\d{2}[-]\d{2}', '2018-02-28 06:03:00.000').group())

    def test_14(self):
        high = '不限定'
        high = '15000待定'
        high = '10000'
        if high == '不限定':
            high = 9999999
        elif re.findall('[\u4e00-\u9fa5]', high):
            high = re.match('\d+', high).group()
        high = int(high)
        print(high)
