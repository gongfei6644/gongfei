from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4


class ParseQ:

    def parse_xpath(self, html_str):
        print(html_str['str'])
        exit()
        dic = {}
        if html_str['str'] == '404':
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dic['d_status'] = 0
            dic['detail_time'] = now_time
            return dic
        if html_str['str'] and html_str['str'] != '404':
            html = etree.HTML(html_str['str'])
            # 解析网页数据  装修情况
            try:
                dic['decoration'] = html.xpath("string(//node()[contains(text(), '装修情况')]/following::node()/text())").strip()
            except Exception as e:
                print(e)
                dic['decoration'] = ''

            # 解析有无电梯   //node()[text()='有无电梯']/following-sibling::*[1]/text()
            try:
                dic['is_elevator'] = html.xpath("string(//node()[contains(text(), '楼梯类型')]/following::text()[1])").strip()
            except Exception as e:
                dic['is_elevator'] = ''
            # 解析产权性质
            try:
                dic['property_nature'] = html.xpath("string(//node()[contains(text(), '房屋用途')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['property_nature'] = ''
            # 住宅类别
            try:
                dic['usage'] = html.xpath("string(//node()[text()='物业类型']/following-sibling::*[1]/text())").strip()
            except Exception as e:
                dic['usage'] = ''
            # 建筑结构
            try:
                dic['building_structure'] = html.xpath("string(//node()[contains(text(), '户型结构')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['building_structure'] = ''
            # 建筑类别
            try:
                dic['building_type'] = html.xpath("//node()[text()='建筑类别']/following-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                dic['building_type'] = ''

            # 小区配套
            try:
                dic['supporting_facilities'] = html.xpath("string(//div[@class='comment_txt fl'])").strip()
            except Exception as e:
                dic['supporting_facilities'] = ''
            if not dic['supporting_facilities']:
                dic['supporting_facilities'] = html.xpath("string(//node()[contains(text(), '周边配套')]/following::text()[1])").strip()
            if '电梯' in dic['supporting_facilities'] or '电梯' in dic['is_elevator']:
                dic['supporting_facilities'] = dic['supporting_facilities'] + '电梯'

            if dic['decoration'] or ['property_nature']:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['d_status'] = 1
                dic['case_happen_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
                dic['detail_time'] = now_time
                return dic
            else:
                dic['d_status'] = 'err'
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['detail_time'] = now_time
                print('当前页面解析不符合规则')
                return dic
