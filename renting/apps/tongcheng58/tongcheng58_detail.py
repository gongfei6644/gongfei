from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4

from utils.unfont import Unfont


class Parse58:

    def parse_xpath(self, html_str):
        # print("进入解析函数...")
        dic = {}
        now_time = datetime.datetime.now()
        dic['detail_time'] = now_time.strftime('%Y-%m-%d %H:%M:%S')
        if html_str['str'] == '404':
            dic['d_status'] = 0
            return dic
        elif html_str['str']:
            try:
                html = etree.HTML(html_str['str'])
                node = html.xpath('//div[@class="house-basic-info"]')[0]
            except:
                print("未找导数据节点{}".format(html_str['link']))
                dic['d_status'] = 'err'
            else:
                try:
                    font_str = re.findall(r"charset=utf-8;base64,(.*?)'\)", html_str['str'], re.S)
                    unfont = Unfont(font_str[0]) if font_str else None
                except:
                    unfont = None
                    # 案例时间
                try:
                    case_happen_date = html.xpath(
                        'string(//p[@class="house-update-info c_888 f12"]/text())').strip()
                    if '分钟' in case_happen_date or '刚刚' in case_happen_date:
                        dic['case_happen_date'] = now_time.strftime('%Y-%m-%d')
                    elif '小时' in case_happen_date:
                        num = re.findall(r'\d+', case_happen_date)[0]
                        dic['case_happen_date'] = (now_time - datetime.timedelta(hours=int(num))).strftime('%Y-%m-%d')
                    elif '天' in case_happen_date:
                        num = re.findall(r'\d+', case_happen_date)[0]
                        dic['case_happen_date'] = (now_time - datetime.timedelta(days=int(num))).strftime('%Y-%m-%d')
                    else:
                        dic['case_happen_date'] = "2019-" + case_happen_date
                except Exception as e:
                    dic['case_happen_date'] = ''
                # 总价
                try:
                    rent = node.xpath('string(.//node()[contains(text(),"元/月")]/*/text())').strip()
                    rent = unfont(rent) if unfont is not None else rent
                    dic['total_price'] = rent
                except:
                    dic['total_price'] = ""
                # 押金方式
                try:
                    dic["deposit_method"] = html.xpath(
                        'string(.//node()[contains(text(),"元/月")]/following-sibling::*[1])').strip()
                except:
                    dic["deposit_method"] = ""
                # 租赁方式
                try:
                    dic["rental_method"] = html.xpath('string(.//span[text()="租赁方式："]/following-sibling::*[1])').strip()
                except:
                    dic["rental_method"] = ""

                try:
                    info1 = node.xpath('string(.//span[text()="房屋类型："]/following-sibling::*[1])').strip()
                    info1 = unfont(info1).replace("\xa0", " ")
                    info1_list = re.split(r'\s\s+', info1)
                    info11 = re.sub(r'\s+', "", info1)
                    build_area = re.findall(r'(\d+\.?\d*)平', info11, re.S)
                    dic['house_type'] = info1_list[0]
                    dic['build_area'] = build_area[0] if build_area else ""
                    dic['decoration'] = info1.split("平")[-1]
                except:
                    dic['house_type'], dic['build_area'], dic['decoration'] = "", "", ""

                try:
                    info2 = node.xpath(
                        'string(.//span[text()="朝向楼层："]/following-sibling::*[1])').replace("\xa0", " ").strip("层 ")
                    info2 = unfont(info2).strip()
                except:
                    dic['orientation'], dic['floor_no'], dic['total_floor_num'] = "", "", ""
                else:
                    try:
                        dic["orientation"] = re.findall(r'[东西南北 ]+', info2)[0]
                    except:
                        dic["orientation"] = ""
                    try:
                        floor_info = info2.strip("东西南北 ")
                        dic["floor_no"] = re.split(r'[共/] ?', floor_info)[0]
                        dic["total_floor_num"] = re.findall(r'\d+', info2)[0]
                    except:
                        dic["total_floor_num"], dic["floor_no"] = "", ""

                # 楼盘
                try:
                    dic['project_name'] = node.xpath(
                        'string(.//span[text()="所在小区："]/following-sibling::*[1]/a)').strip()
                except:
                    dic['project_name'] = ''

                # 行政区:
                try:
                    dic['area'] = node.xpath(
                        'string(.//span[text()="所属区域："]/following-sibling::*[1]/a[1])').strip()
                except:
                    dic['area'] = ''

                # 地址
                try:
                    dic['address'] = node.xpath('string(//span[text()="详细地址："]/following-sibling::*[1])').strip()
                except:
                    dic['address'] = ""
                # 配套
                try:
                    supporting_list = html.xpath('//ul[@class="house-disposal"]/li[not(@class="icon")]//text()')
                    dic['supporting_facilities'] = "、".join(supporting_list)
                except:
                    dic['supporting_facilities'] = ""

                if dic['case_happen_date'] and dic['project_name']:
                    dic['d_status'] = 1
                else:
                    dic['d_status'] = "err"
                    print('当前页面解析不符合规则')
        else:
            dic['d_status'] = "err"

        # 补充字段
        dic['build_type'] = ""
        dic['house_structure'] = ""
        dic['affiliated_house'] = ""
        dic["build_date"] = ""
        dic['remaining_years'] = ""
        dic['new_ratio'] = ""
        dic['build_name'] = ""
        dic['house_name'] = ""
        dic['usable_area'] = ""
        dic['currency'] = "人民币"
        dic['case_type'] = "月平方米租报盘"
        print(dic)
        return dic
