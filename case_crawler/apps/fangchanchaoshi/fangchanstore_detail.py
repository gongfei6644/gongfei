from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4


class ParseFangStore:

    def parse_xpath(self, html_str):
        dic = {}
        if html_str['str'] == '404':
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dic['d_status'] = 0
            dic['detail_time'] = now_time
            return dic
        if html_str['str'] and html_str['str'] != '404':
            html = etree.HTML(html_str['str'])
            # 朝向
            try:
                dic['orientation'] = html.xpath("string(//node()[contains(text(), '房屋朝向')]/following::node()/text())").strip()
            except Exception as e:
                print(e)
                dic['orientation'] = ''
            # 装修
            try:
                dic['decoration'] = html.xpath("string(//node()[contains(text(), '装修程度')]/following-sibling::node()/text())").strip()
            except Exception as e:
                print(e)
                dic['decoration'] = ''
            # 解析有无电梯   //node()[text()='有无电梯']/following-sibling::*[1]/text()
            try:
                dic['is_elevator'] = html.xpath("//node()[text()='有无电梯']/following-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                dic['is_elevator'] = ''
            # 解析产权性质
            try:
                dic['property_nature'] = html.xpath("string(//node()[contains(text(), '产权类型：')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['property_nature'] = ''
            # 住宅类别
            try:
                dic['usage'] = html.xpath("string(//node()[contains(text(), '楼型用途')]/following-sibling::node()/text())").strip().split('/')[1]
            except Exception as e:
                dic['usage'] = ''
            # 建筑结构
            try:
                dic['building_structure'] = html.xpath("string(//node()[contains(text(), '楼型用途')]/following-sibling::node()/text())").strip().split('/')[0]
            except Exception as e:
                dic['building_structure'] = ''
            # 建筑类别
            try:
                dic['building_type'] = html.xpath("//node()[text()='建筑类别']/following-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                dic['building_type'] = ''
            # 挂牌时间 案例时间
            # case_happen_date
            try:
                dic['case_happen_date'] = html.xpath("string(//node()[@class='pr10'][1])").strip().replace('发布', '')
            except Exception as e:
                dic['case_happen_date'] = ''

            # 建筑年代
            # try:
            #     dic['build_date'] = html.xpath("string(//node()[contains(text(), '建造年代：')]/following-sibling::node()/text())").strip()
            # except Exception as e:
            #     dic['build_date'] = ''

            # 小区配套
            try:
                dic['supporting_facilities'] = html.xpath("string(//node()[contains(text(), '房源描述')]/following-sibling::div)").strip()
            except Exception as e:
                dic['supporting_facilities'] = ''

            # 联系电话
            try:
                dic['tel'] = html.xpath("string(//span[@id='mobilecode'])")
            except Exception as e:
                dic['tel'] = ''

            if dic['case_happen_date'] or dic['decoration'] or dic['property_nature']:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['d_status'] = 1
                dic['detail_time'] = now_time
                if dic['is_elevator'] == '有':
                    if dic['supporting_facilities']:
                        dic['supporting_facilities'] = dic['supporting_facilities'] + ',电梯'
                    else:
                        dic['supporting_facilities'] = dic['supporting_facilities'] + '电梯'
                return dic
            else:
                dic['d_status'] = 'err'
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['detail_time'] = now_time
                # print('当前页面解析不符合规则')
                return dic
