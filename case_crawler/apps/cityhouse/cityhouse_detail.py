from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4


class CityHouse:

    def parse_xpath(self, html_str):
        dic = {}
        if html_str['str'] == '404':
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dic['d_status'] = 1
            dic['detail_time'] = now_time
            return dic
        if html_str['str'] and html_str['str'] != '404':
            html = etree.HTML(html_str['str'])
            # 装修情况
            try:
                dic['decoration'] = html.xpath("string(//node()[contains(text(),'装修程度')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['decoration'] = ''
            # 用途
            try:
                dic['usage'] = html.xpath("string(//node()[contains(text(),'用途')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['usage'] = ''
            # 产权性质
            try:
                dic['property_nature'] = html.xpath(
                    "string(//node()[contains(text(),'权属')]/following-sibling::node()/text())").replace('-', '')
            except Exception as e:
                dic['property_nature'] = ''
            # 有无电梯
            try:
                dic['is_elevator'] = html.xpath(
                    "string(//node()[contains(text(), '配备电梯')]/following::node()/text())").strip()
            except Exception as e:
                dic['id_elevator'] = ''

            # 配套
            try:
                dic['supporting_facilities'] = html.xpath(
                    "string(//node()[contains(text(),'附属设施')]/following-sibling::node()/text())").strip()
                if '电梯' in dic['supporting_facilities']:
                    dic['supporting_facilities'] = '电梯'
                else:
                    dic['supporting_facilities'] = ''
            except Exception as e:
                dic['supporting_facilities'] = ''
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dic['d_status'] = 1
            dic['detail_time'] = now_time
            print(dic)
            return dic

#             # dic['test'] = 1
#             dic['detail_time'] = now_time
#             # if dic['is_elevator'] == '有':
#             #     if dic['supporting_facilities']:
#             #         dic['supporting_facilities'] = dic['supporting_facilities'] + ',电梯'
#             #     else:
#             #         dic['supporting_facilities'] = dic['supporting_facilities'] + '电梯'
#             return dic
# >>>>>>> c2a7fae4ed949ea205aba43fa10ef423e6217b12
