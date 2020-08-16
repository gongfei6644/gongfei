from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4


class ParseZy:

    def parse_xpath(self, html_str):
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
                dic['decoration'] = html.xpath("string(//node()[@class='small']/node()[@class='m_2'])").strip()
            except Exception as e:
                dic['decoration'] = ''
            # 解析有无电梯   //node()[text()='有无电梯']/following-sibling::*[1]/text()
            try:
                dic['is_elevator'] = html.xpath("string(//node()[contains(text(), '楼梯类型')]/following::text()[1])").strip()
            except Exception as e:
                dic['is_elevator'] = ''
            # 解析产权性质
            try:
                dic['property_nature'] = html.xpath("string(//node()[text()='产权性质']/following-sibling::*[1]/text())").strip()
            except Exception as e:
                dic['property_nature'] = ''
            # 住宅类别
            try:
                dic['usage'] = html.xpath("string(//node()[text()='物业类型']/following-sibling::*[1]/text())").strip()
            except Exception as e:
                dic['usage'] = ''
            # 建筑结构
            try:
                dic['building_structure'] = html.xpath("//node()[text()='建筑结构']/following-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                dic['building_structure'] = ''
            # 建筑类别
            try:
                dic['building_type'] = html.xpath("//node()[text()='建筑类别']/following-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                dic['building_type'] = ''
            # 挂牌时间 案例时间
            try:
                dic['case_happen_date'] = html.xpath("string(//node()[@class='labeltag']/node()[contains(text(), '更新')])").strip()
                if '前' in dic['case_happen_date']:
                    num = re.findall(r'\d+', dic['case_happen_date'])[0]
                    dic['case_happen_date'] = (datetime.datetime.now() + datetime.timedelta(days=-int(num))).strftime('%Y-%m-%d')
                if '内' in dic['case_happen_date']:
                    dic['case_happen_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            except Exception as e:
                print(e)
                dic['case_happen_date'] = ''
            if '更新' in dic['case_happen_date']:
                dic['case_happen_date'] = dic['case_happen_date'].replace('更新', '')
            if '/' in dic['case_happen_date']:
                dic['case_happen_date'] = dic['case_happen_date'].replace('/', '-')

            # 建筑年代
            try:
                dic['build_date'] = re.findall('\d+', html.xpath("string(//node()[@class='small']/node()[@class='m_3'])").strip())[0]
            except Exception as e:
                dic['build_date'] = ''

            # 小区配套
            try:
                dic['supporting_facilities'] = html.xpath("string(//div[@class='comment_txt fl'])").strip()
            except Exception as e:
                dic['supporting_facilities'] = ''
            if not dic['supporting_facilities']:
                dic['supporting_facilities'] = html.xpath("string(//node()[contains(text(), '周边配套')]/following::text()[1])").strip()
            if '电梯' in dic['supporting_facilities'] or '电梯' in dic['is_elevator']:
                dic['supporting_facilities'] = dic['supporting_facilities'] + '电梯'

            # 联系电话
            try:
                dic['tel'] = html.xpath("string(//span[@id='mobilecode'])")
            except Exception as e:
                dic['tel'] = ''

            if dic['build_date'] or dic['decoration'] or ['case_happen_date']:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['d_status'] = 1
                dic['detail_time'] = now_time
                return dic
            else:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['d_status'] = 'err'
                dic['detail_time'] = now_time
                return dic




