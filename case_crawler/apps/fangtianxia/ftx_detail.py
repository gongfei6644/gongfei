from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4

# string(//node()[contains(text(), '楼层')]/preceding-sibling::node()[2])
class FangParse:

    def parse_xpath(self, html_str):
        dic = {}
        if html_str['str'] == '404':
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dic['d_status'] = 0
            dic['detail_time'] = now_time
            return dic
        elif html_str['str'] and html_str['str'] != '404':
            html = etree.HTML(html_str['str'])
            # 所在楼层
            try:
                floor_no1 = html.xpath("string(//node()[contains(text(), '楼层')]/preceding-sibling::node()[2])").strip()
                floor_no = html.xpath('string(//node()[contains(text(), "层数")]/preceding-sibling::*[1]/text())').strip()
                if floor_no or floor_no1:
                    dic['floor_no'] = floor_no or floor_no1
                else:
                    dic['floor_no'] = ''

            except:
                pass
            # 总楼层
            try:
                total_floor_num = re.findall('\d+', html.xpath('string(//node()[contains(text(), "层数")])'))[0]
                if total_floor_num:
                    dic['total_floor_num'] = total_floor_num
            except:
                pass

            # 户型
            try:
                dic['house_type'] = html.xpath("string(//node()[text()='户型']/preceding-sibling::*[1]/text())").strip()
            except Exception as e:
                dic['house_type'] = ''

            # 解析网页数据  装修情况
            try:
                dic['decoration'] = html.xpath("//node()[text()='装修']/preceding-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                # print(e)
                dic['decoration'] = ''
            # 解析有无电梯   //node()[text()='有无电梯']/following-sibling::*[1]/text()
            try:
                dic['is_elevator'] = html.xpath("//node()[text()='有无电梯']/following-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                dic['is_elevator'] = ''
            # 解析产权性质
            try:
                dic['property_nature'] = html.xpath("//node()[text()='产权性质']/following-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                dic['property_nature'] = ''
            # 住宅类别
            try:
                dic['usage'] = html.xpath("//node()[text()='住宅类别']/following-sibling::*[1]/text()")[0].strip()
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
            # case_happen_date
            try:
                dic['case_happen_date'] = html.xpath("//node()[text()='挂牌时间']/following-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                dic['case_happen_date'] = ''

            # 建筑年代
            try:
                dic['build_date'] = html.xpath("//node()[text()='建筑年代']/following-sibling::*[1]/text()")[0].strip()
            except Exception as e:
                dic['build_date'] = ''

            # 小区配套
            try:
                dic['supporting_facilities'] = html.xpath("string(//node()[text()='小区配套']/following-sibling::div[1]/text())").strip()
            except Exception as e:
                # 小区配套
                try:
                    dic['supporting_facilities'] = \
                    html.xpath("string(//node()[text()='小区配套']/following-sibling::div[1]/text())")[0].strip()
                except Exception as e:
                    dic['supporting_facilities'] = ''
            # 联系电话
            try:
                dic['tel'] = html.xpath("string(//span[@id='mobilecode'])")
            except Exception as e:
                dic['tel'] = ''

            if dic['case_happen_date'] or dic['build_date'] or dic['decoration']:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['d_status'] = 1
                dic['detail_time'] = now_time
                if dic['is_elevator'] == '有':
                    dic['supporting_facilities'] = '电梯'
                else:
                    dic['supporting_facilities'] = ''
                return dic
            else:
                dic['d_status'] = 'err'
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['detail_time'] = now_time
                # print('当前页面解析不符合规则')
                return dic
