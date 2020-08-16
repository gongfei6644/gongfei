# coding: utf-8
import datetime
import re

import requests
from lxml import etree


class ParseDemo():
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

        elif html_str['str'] and html_str['str'] != '404':

            # 解析网页数据
            try:
                expired1 = re.findall(r"下架", html_str['str'], re.S)
                expired2 = re.findall(r"forbidden", html_str['str'], re.S)
                if any([expired1, expired2]):
                    item['d_status'] = 0
                    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    item['detail_time'] = now_time
                    return item
            except:
                pass

            html = etree.HTML(html_str['str'])
            try:
                floor_info = html.xpath('string(//span[text()="所在楼层："]/following-sibling::*[1]/text())')
                total_floor_num = re.findall(r'共(\d+)层', floor_info, re.S)[0]
            except:
                total_floor_num = ""
            try:
                decoration = html.xpath('string(//span[text()="房屋装修："]/following-sibling::*[1]/text())').strip()  # 装修档次
                building_type = html.xpath(
                    'string(//li[@class="info-item"]/span[text()="建筑类型："]/following-sibling::*[1]/text())').strip()  # 建筑类型

                is_elevator = html.xpath(
                    'string(//li[@class="info-item"]/span[text()="配备电梯："]/following-sibling::span[1]/text())').strip()  # 电梯

            except:
                decoration, building_type, case_happen_date, is_elevator = "", "", "", ""

            item["detail_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 补录时间
            item["total_floor_num"] = total_floor_num  # 总楼层
            item["decoration"] = decoration  # 装修档次
            item["building_type"] = building_type  # 建筑类型
            item["is_elevator"] = is_elevator  # 是否有电梯
            item["supporting_facilities"] = "电梯" if "有" == is_elevator else ""
            item["d_status"] = 1
            return item
        else:
            print('str为空')
