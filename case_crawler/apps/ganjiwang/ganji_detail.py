from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4


class ParseGanji:

    def parse_xpath(self, html_str):

        dic = {}
        if html_str['str'] == '404':
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dic['d_status'] = 0
            dic['detail_time'] = now_time
            return dic
        if html_str['str'] and html_str['str'] != '404':
            html = etree.HTML(html_str['str'])

            # 解析网页数据
            # # 楼层
            # floor_buffer = html.xpath("string(//node()[contains(text(), '层')])").strip()
            # if floor_buffer:
            #     if '/' in floor_buffer:
            #         try:
            #             dic['floor_no'] = floor_buffer.split('/')[0]
            #         except Exception as e:
            #             dic['floor_no'] = ''
            #         try:
            #             dic['total_floor_num'] = floor_buffer.split('/')[1]
            #         except Exception as e:
            #             dic['total_floor_num'] = ''
            # else:
            #     dic['floor_no'] = ''
            #     dic['total_floor_num'] = ''
            # 装修情况
            try:
                dic['decoration'] = html.xpath("string(//node()[contains(text(), '装修情况')]/following-sibling::node())").strip()
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
                # string(//node()[@class='t' and contains(text(), '产')]/following-sibling::*[1])
                dic['property_nature'] = html.xpath("string(//node()[contains(text(), '产权性质')]/following-sibling::node())").strip()
            except Exception as e:
                dic['property_nature'] = ''
            # 住宅类别
            try:
                dic['usage'] = html.xpath("string(//node()[contains(text(), '住宅类别')]/following-sibling::node())").strip()
            except Exception as e:
                dic['usage'] = ''
            # 建筑结构
            try:
                dic['building_structure'] = html.xpath("string(//node()[contains(text(), '建筑结构')]/following-sibling::node())").strip()
            except Exception as e:
                dic['building_structure'] = ''
            # 建筑类别
            try:
                dic['building_type'] = html.xpath("string(//node()[contains(text(), '建筑类别')]/following-sibling::node())").strip()
            except Exception as e:
                dic['building_type'] = ''
            # 挂牌时间 案例时间
            # case_happen_date
            try:
                dic['case_happen_date'] = html.xpath("string(//node()[@class='date'])").strip()
                case_happen_date = html.xpath("string(//node()[@class='date'])").strip()
                if '小时' in case_happen_date or '分' in case_happen_date or '刚刚' in case_happen_date:
                    dic['case_happen_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
                if '天' in case_happen_date:
                    num = re.findall(r'\d+', case_happen_date)[0]
                    dic['case_happen_date'] = (datetime.datetime.now() + datetime.timedelta(days=-int(num))).strftime \
                        ('%Y-%m-%d')

            except Exception as e:
                dic['case_happen_date'] = ''

            # 建筑年代
            try:
                dic['build_date'] = html.xpath("string(//node()[contains(text(),'建筑年代')]/following-sibling::node())").strip()
            except Exception as e:
                dic['build_date'] = ''

            # 小区配套
            try:
                dic['supporting_facilities'] = html.xpath("string(//node()[@class='describe'])").strip().replace('\n',
                                                                                                                 '')
                if '电梯' in dic['supporting_facilities']:
                    dic['supporting_facilities'] = '电梯'
                else:
                    dic['supporting_facilities'] = ''
            except Exception as e:
                dic['supporting_facilities'] = ''

            # 联系电话
            # try:
            #     dic['tel'] = html.xpath("string(//node()[@class='phone_num js_person_phone'])")
            # except Exception as e:
            #     dic['tel'] = ''

            # 解析所在地址
            try:
                dic['address'] = html.xpath("string(//node()[contains(text(),'所在地址')]/following-sibling::node()/text())").strip()
            except Exception as e:
                dic['address'] = ''

            if dic['build_date'] or dic['case_happen_date']:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['d_status'] = 1
                dic['detail_time'] = now_time
                if dic['is_elevator'] == '有':
                    if dic['supporting_facilities']:
                        dic['supporting_facilities'] = dic['supporting_facilities'] + ',电梯'
                    else:
                        dic['supporting_facilities'] = dic['supporting_facilities'] + '电梯'
            else:
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dic['detail_time'] = now_time
                dic['d_status'] = 'err'
            return dic

