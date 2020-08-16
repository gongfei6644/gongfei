# -*- coding: utf-8 -*-


import unittest

from app.service.std import *


class StdTestCase(unittest.TestCase):
    def test_deal_decoration(self):
        case = Case()
        case.decoration = '豪华'
        deal_decoration(case, None)

    def test_deal_house_type(self):
        case = Case()
        # case.house_type = '四室零厅'
        # case.house_type = '3厅四室'
        # case.house_type = '6厅四室'
        # case.house_type = '2卫零厅一室'
        # case.house_type = '2卫三厅五室'
        # case.house_type = '2卫三厅八室'
        # case.house_type = '2卫三厅三室'
        case.house_type = '2卫三厅一室'
        std_case = StdCase()
        deal_house_type(case, std_case)
        print(std_case.house_type)

    def test_trim_case(self):
        case = Case()
        case.project_name = '李兴 花园  '
        case.case_happen_date = ' 2019-09-09 '
        case.usage = 'xx xx x x'
        case.house_area = 'd2323'
        trim_case(case)
        print(case)

    def test_deal_district(self):
        case = Case()
        case.city = '宁波市'
        case.area = '镇海'
        std_case = StdCase()
        deal_district(case, std_case)

    def test_str_replace(self):
        dt = '2019-1-2'
        dt = re.match('\d{4}[-]\d+[-]\d+', dt).group()
        print(dt)
        splits = dt.split('-')
        dt2 = splits[0] + '-'
        if splits[1].__len__() == 1:
            dt2 += '0' + splits[1] + '-'
        else:
            dt2 += splits[1] + '-'
        if splits[2].__len__() == 1:
            dt2 += '0' + splits[2]
        else:
            dt2 += splits[2]
        print(dt2)

    def test_house_area(self):
        house_area = "90.333344"
        house_area = '90.3'

        ret = "{:.2f}".format(float(house_area))
        print(ret)

    def test_get_area_alias(self):
        a = get_area_alias('xxx区县')
        print(a)

    def test_deal_project_name(self):
        # s = '东方小区(镜湖)'
        # area = '镜湖区'
        # area = area.replace('县', '').replace('区', '')
        # m = re.findall('[（(]+.+[)）]+', s)
        # if m and m[0].__contains__(area):
        #     idx = s.find('（')
        #     if idx == -1:
        #         idx = s.find('(')
        #     s = s[0:idx]
        # print(s)

        # def match(project_name):
        #     m = re.findall('（.*[路道号街巷]+.*）|（.*别墅.*）|（.*公寓.*）', project_name)
        #     if not m:
        #         m = re.findall('\(.*[路道号街巷]+.*\)|\(.*别墅.*\)|\(.*公寓.*\)', project_name)
        #     if m:
        #         r = m[0]
        #         print("project_name: {}, match: {}, replace: {}".
        #               format(project_name, r, project_name.replace(r, '')))
        #     else:
        #         print("project_name: {}, match: null".format(project_name))
        #
        # match('鼓浪屿花园（xxx路）二期')
        # match('鼓浪屿花园（xxx巷）')
        # match('鼓浪屿花园（xxx公寓）二期')
        # match('鼓浪屿花园（xxx公）二期')
        # match('鼓浪屿花园（xxx湖）')
        #
        # match('鼓浪屿花园(xxx路)二期')
        # match('鼓浪屿花园(xxx巷)')
        # match('鼓浪屿花园(xxx公寓)二期')
        # match('鼓浪屿花园(xxx公)二期')
        # match('鼓浪屿花园(xxx湖)')
        #
        print(deal_project_name('鼓浪屿花园（xxx车库）二期', city='深圳市', area='南山区'))
        print(deal_project_name('鼓浪屿花园(xxx后面)二期'))
        print(deal_project_name('鼓浪屿花园（xxx栋）二期'))
        print(deal_project_name('鼓浪屿花园(xxx路)二期'))

        print(deal_project_name('鼓浪屿花园（xxx商住楼**）二期'))
        print(deal_project_name('鼓浪屿花园（xxx备案名**）二期'))
        print(deal_project_name('鼓浪屿花园南山区12栋xxx（xxx商住楼**）二期', area='南山区'))
        print(deal_project_name('鼓浪屿花园南山区栋xxx（xxx商住楼**）二期', area='南山区'))
        print(deal_project_name('鼓浪屿花园南山区12单元xxx（xxx商住楼**）二期', area='南山区'))

        print(deal_project_name('鼓浪屿花园（xxx路）二期'))
        print(deal_project_name('鼓浪屿花园（xxx巷）'))
        print(deal_project_name('鼓浪屿花园（xxx公寓）二期'))
        print(deal_project_name('鼓浪屿花园（xxx公）二期'))
        print(deal_project_name('鼓浪屿花园（xxx湖）'))

        print(deal_project_name('鼓浪屿花园(xxx巷)'))
        print(deal_project_name('鼓浪屿花园(xxx公寓)二期'))
        print(deal_project_name('鼓浪屿花园(xxx公)二期'))
        print(deal_project_name('鼓浪屿花园(xxx湖)'))

        print(deal_project_name('华杰善水公馆(重庆路)', ''))

        print(deal_project_name('鼓浪屿花园一室2厅'))
        print(deal_project_name('鼓浪屿花园3室'))

