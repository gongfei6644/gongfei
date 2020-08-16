from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4


class Parse58:

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
            # 朝向
            try:
                dic['orientation'] = html.xpath("string(//node()[contains(text(), '房屋朝向')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['orientation'] = ''
            # 装修
            try:
                dic['decoration'] = html.xpath("string(//node()[contains(text(), '装修情况')]/following-sibling::node()/text())").strip()
            except Exception as e:
                # print(e)
                dic['decoration'] = ''
            # 未解析
            # 解析有无电梯   //node()[text()='有无电梯']/following-sibling::*[1]/text()
            try:
                dic['is_elevator'] = html.xpath("string(//node()[contains(text(), '有无电梯')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['is_elevator'] = ''
            # 解析产权性质
            try:
                dic['property_nature'] = html.xpath("string(//node()[contains(text(), '交易权属')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['property_nature'] = ''
            # 住宅类别
            try:
                dic['usage'] = html.xpath("string(//node()[contains(text(), '房屋类型')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['usage'] = ''
            # 建筑结构
            try:
                dic['building_structure'] = html.xpath("string(//node()[contains(text(), '建筑结构')]/following-sibling::node()/text())")[0].strip()
            except Exception as e:
                dic['building_structure'] = ''
            # 建筑类别
            try:
                dic['building_type'] = html.xpath("string(//node()[contains(text(), '建筑类别')]/following-sibling::node()/text())")[0].strip()
            except Exception as e:
                dic['building_type'] = ''
            # 未解析
            # 挂牌时间 案例时间
            # case_happen_date
            try:
                # print('-----xpath', html.xpath("//node()[text()='挂牌时间']/following-sibling::*[1]/text()"))
                case_happen_date = html.xpath("string(//node()[@class='up'][1])").strip()
                dic['case_happen_date'] = case_happen_date
                if '小时' in case_happen_date or '分钟' in case_happen_date or '刚刚' in case_happen_date:
                    dic['case_happen_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
                if '天' in case_happen_date:
                    num = re.findall(r'\d+', case_happen_date)[0]
                    dic['case_happen_date'] = (datetime.datetime.now() + datetime.timedelta(days=-int(num))).strftime('%Y-%m-%d')
            except Exception as e:
                dic['case_happen_date'] = ''

            # 建筑年代
            try:
                dic['build_date'] = html.xpath("string(//node()[contains(text(), '建筑年代')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['build_date'] = ''
            try:
                dic['supporting_facilities'] = html.xpath("string(//node()[contains(text(), '描述')]/following-sibling::div)").strip().replace('\n', '')
                if '电梯' in dic['supporting_facilities']:
                    dic['supporting_facilities'] = '电梯'
                else:
                    dic['supporting_facilities'] = ''
            except Exception as e:
                dic['supporting_facilities'] = ''
            # 楼层处理
            floor_buffer = html.xpath(
                "string(//node()[contains(text(),'所在楼层')]/following-sibling::node()/text())").strip()
            if floor_buffer:
                if '/' in floor_buffer:
                    dic['floor_no'] = floor_buffer.split('/')[0]
                    try:
                        dic['total_floor_num'] = re.findall(r'\d+', floor_buffer.split('/')[1])[0]
                    except Exception as e:
                        # print('floor', e)
                        dic['total_floor_num'] = ''

                else:
                    if '共' in floor_buffer:
                        dic['floor_no'] = ''
                        dic['total_floor_num'] = re.findall(r'\d+', floor_buffer)[0]
                    else:
                        dic['floor_no'] = re.findall(r'\d+', floor_buffer)[0]
                        dic['total_floor_num'] = ''
            else:
                dic['floor_no'] = ''
                dic['total_floor_num'] = ''

            if dic['case_happen_date'] or dic['build_date']:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['d_status'] = 1
                # dic['test'] = 1
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
                print('当前页面解析不符合规则')
                return dic
