from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4


class ParseLianJ:

    def parse_xpath(self, html_str):

        dic = {}
        if html_str['str'] == '404':
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dic['d_status'] = 0
            dic['detail_time'] = now_time
            return dic
        if html_str['str'] and html_str['str'] != '404':
            html = etree.HTML(html_str['str'])
            try:
                dic["project_name"] = html.xpath('string(//span[contains(text(), "小区名称")]/following-sibling::*[1]/text())')
            except:
                dic["project_name"] = ""
            # 建筑面积
            try:
                house_area = html.xpath('string(//span[contains(text(), "建筑面积")]/parent::*[1]/text())').replace("㎡", "")
                if house_area:
                    dic["house_area"] = house_area
            except:
                pass

            # 装修情况
            try:
                dic['decoration'] = html.xpath("string(//node()[contains(text(), '装修情况')]/following::text()[1])").strip()
            except Exception as e:
                dic['decoration'] = ''
            # 解析有无电梯   //node()[text()='有无电梯']/following-sibling::*[1]/text()
            try:
                dic['is_elevator'] = html.xpath("string(//node()[contains(text(), '配备电梯')]/following::text()[1])").strip()
            except Exception as e:
                dic['is_elevator'] = ''
            # 解析产权性质
            try:
                dic['property_nature'] = html.xpath("string(//node()[contains(text(), '交易权属')]/following::node()/text())").strip()
            except Exception as e:
                dic['property_nature'] = ''
            # 住宅类别
            try:
                dic['usage'] = html.xpath("string(//node()[contains(text(), '房屋用途')]/following::node()/text())").strip()
            except Exception as e:
                dic['usage'] = ''
            # 建筑结构
            try:
                dic['building_structure'] = html.xpath("string(//node()[contains(text(), '建筑结构')]/following::text())").strip()
            except Exception as e:
                dic['building_structure'] = ''
            # 建筑类别
            try:
                dic['building_type'] = html.xpath("string(//node()[contains(text(), '建筑类型')]/following::text())").strip()
            except Exception as e:
                dic['building_type'] = ''
            # 挂牌时间 案例时间
            # case_happen_date
            try:
                dic['case_happen_date'] = html.xpath("string(//node()[contains(text(), '挂牌时间')]/following::node()/text())").strip()
            except Exception as e:
                dic['case_happen_date'] = ''

            #  户型结构
            try:
                dic['house_structure'] = html.xpath("string(//node()[contains(text(),'户型结构')]/following::text()[1])").strip()
            except Exception as e:
                dic['house_structure'] = ''

            # 套内面积
            try:
                dic['inside_space'] = html.xpath("string(//node()[contains(text(),'套内面积')]/following::text()[1])").strip()
                if '㎡' in dic['inside_space']:
                    dic['inside_space'] = dic['inside_space'].replace('㎡', '')
            except Exception as e:
                dic['inside_space'] = ''

            # 小区配套
            try:
                dic['supporting_facilities'] = html.xpath("string(//node()[contains(text(), '周边配套')]/following-sibling::node()/text()[1])").strip().replace('\n', '')
            except Exception as e:
                dic['supporting_facilities'] = ''

            # 解析所在地址
            try:
                dic['address'] = html.xpath("string(//node()[contains(text(), '所在区域')]/following-sibling::a/text())").strip()
            except Exception as e:
                dic['address'] = ''

            if dic['case_happen_date'] or dic['decoration']:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['d_status'] = 1
                dic['detail_time'] = now_time
                if dic['is_elevator'] == '有':
                    if dic['supporting_facilities']:
                        dic['supporting_facilities'] = dic['supporting_facilities'] + ',电梯'
                    else:
                        dic['supporting_facilities'] = dic['supporting_facilities'] + '电梯'
                print(dic)
                return dic
            else:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['d_status'] = 'err'
                dic['detail_time'] = now_time
                return dic
