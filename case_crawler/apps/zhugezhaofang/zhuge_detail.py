# coding: utf-8
import datetime
import re

import requests
from lxml import etree

from utils.constants import PATTTERN_MAP


class ParseZhuge():
    """
    诸葛找房解析类
    """

    def parse_xpath(self, html_str):
        item = {}
        if html_str['str'] == '404':
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['d_status'] = 0
            item['detail_time'] = now_time
            return item

        elif html_str['str'] and html_str['str']:

            # 解析网页数据
            html = etree.HTML(html_str['str'])
            clean_str = PATTTERN_MAP["blank"].sub("", html_str['str'])
            try:
                expired1 = re.findall(r"下架", clean_str)
                expired2 = re.findall(r"forbidden", clean_str)
                if any([expired1, expired2]):
                    item['d_status'] = 0
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    item['detail_time'] = now_time
                    return item
            except:
                pass
            try:
                project_name1 = html.xpath('string(//div[@class="housing-village"]/a)')
                project_name2 = html.xpath('string(//span[contains(text(), "小区名称")]/following-sibling::*[1]/text())')
                item["project_name"] = project_name1 or project_name2
            except:
                item["project_name"] = ""
            try:
                total_floor_num = PATTTERN_MAP["zhuge_floor"].findall(clean_str)
                item["total_floor_num"] = total_floor_num[0]
            except:
                item["total_floor_num"] = ""
            try:
                house_type2 = PATTTERN_MAP["house_type"].findall(clean_str)[0]  # 房屋户型
                house_type_list = html.xpath('//p[contains(text(), "房屋户型")]/preceding-sibling::p[1]/text()')
                house_type1 = re.sub('\s+', '', "".join(house_type_list), re.S)
                house_type = "".join(house_type1) or house_type2
                if house_type:
                    item["house_type"] = house_type
            except:
                pass

            try:
                decoration = html.xpath('string(//span[text()="房屋装修："]/following-sibling::*[1]/text())').strip()  # 装修档次
                build_date = html.xpath('string(//span[text()="建筑年代："]/following-sibling::*[1]/text())').strip()  # 建筑年代
                building_type = html.xpath(
                    'string(//li[@class="info-item"]/span[text()="建筑类型："]/following-sibling::*[1]/text())').strip()  # 建筑类型

                is_elevator = html.xpath(
                    'string(//li[@class="info-item"]/span[text()="配备电梯："]/following-sibling::span[1]/text())').strip()  # 电梯
                case_happen_date = html.xpath('string(//li[contains(text(), "更新时间")]/span/text())').strip()
            except:
                decoration, building_type, case_happen_date, is_elevator, build_date = "", "", "", "", ""
            item["detail_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 补录时间
            # item["house_type"] = house_type
            # item["total_floor_num"] = total_floor_num  # 总楼层
            item["decoration"] = decoration  # 装修档次
            item["building_type"] = building_type  # 建筑类型
            item["is_elevator"] = is_elevator  # 是否有电梯
            item["supporting_facilities"] = "电梯" if "有" == is_elevator else ""
            item["case_happen_date"] = case_happen_date
            item["d_status"] = 1
            if build_date:
                item["build_date"] = build_date
            return item
        else:
            print('str为空')
