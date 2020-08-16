from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4
from utils.constants import PATTTERN_MAP
from utils.unfont import Unfont


class KeParse:

    def parse_xpath(self, html_str):
        # print('======================html_str===========================')
        dic = {}
        now_time = datetime.datetime.now()
        dic['detail_time'] = now_time.strftime('%Y-%m-%d %H:%M:%S')
        dic['d_status'] = 1
        if html_str['str'] == '404':
            dic['d_status'] = 0
            return dic
        elif html_str['str'] == '访问页面不存在':
            dic['d_status'] = "Page missing"
            return dic
        elif html_str['str']:
            font_str = re.findall(r"charset=utf-8;base64,(.*?)'\)", html_str['str'], re.S)
            unfont = Unfont(font_str[0]) if font_str else None
            try:
                html = etree.HTML(html_str['str'])
            except:
                dic['d_status'] = "err"
                print("无效案例")
            else:
                # 发布时间
                try:
                    happen_date = html.xpath('string(//div[contains(text(), "发布时间：")]//b)')
                    happen_date = unfont(happen_date) if unfont else happen_date
                    date = re.findall('(\d+)年(\d+)月(\d+)', happen_date, re.S)
                    dic['case_happen_date'] = "-".join(date[0])
                    # period = datetime.datetime.strptime(dic['case_happen_date'], '%Y-%m-%d')
                    # if abs(period) > 15:

                    #     dic['d_status'] = "err"
                    if dic['case_happen_date'] > now_time.strftime('%Y-%m-%d') or dic['case_happen_date'] < '2017-01-01':
                        return
                except:
                    dic['case_happen_date'] = ""

                # 租赁方式
                try:
                    dic["rental_method"] = html.xpath('string(//li[@class="title-label-item rent"])').strip()
                except:
                    dic["rental_method"] = ""
                # 租金
                try:
                    total_price = html.xpath('string(//span[@class="price"]//b)').strip()
                    unit = html.xpath('string(//span[@class="price"])')
                    total_price = float(unfont(total_price)) if unfont else float(total_price)
                    dic["total_price"] = total_price * 10000 if "万" in unit else total_price
                except:
                    dic['total_price'] = ""
                # 押金方式
                try:
                    dic["deposit_method"] = html.xpath('string(string(.//span[@class="type"]))').strip()
                except:
                    dic["deposit_method"] = ""

                # 户型
                try:
                    house_type = html.xpath('string(//span[contains(text(), "户型：")]/following-sibling::*[1])').strip()
                    dic["house_type"] = unfont(house_type)

                except:
                    dic["house_type"] = ""
                    # 面积
                try:
                    build_area = html.xpath('string(//span[contains(text(), "面积：")]/following-sibling::*[1])').strip(
                        "平方米 ")
                    dic["build_area"] = int(float(unfont(build_area))) if unfont else float(build_area)
                except:
                    dic["build_area"] = ""
                # 朝向
                try:
                    dic['orientation'] = html.xpath(
                        'string(//span[contains(text(), "朝向：")]/following-sibling::*[1])').strip()
                except:
                    dic['orientation'] = ''
                # 楼层
                try:
                    floor = html.xpath(
                        'string(//span[contains(text(), "楼层：")]/following-sibling::*[1])').strip()
                    floor = unfont(floor)
                    floor_list = re.split(r'[\\(/]', floor)
                    total_floor_num = re.findall(r'\d+', floor_list[-1])
                    floor_no1 = re.findall(r'[底低中高]层', floor_list[0])
                    floor_no1 = floor_no1[0] if floor_no1 else ""
                    floor_no2 = re.findall(r'\d+', floor_list[0])
                    floor_no2 = floor_no2[0] if floor_no2 else ""

                    dic['floor_no'] = floor_no1 or floor_no2
                    dic['total_floor_num'] = total_floor_num[0] if total_floor_num else ""

                except:
                    dic["floor_no"], dic["total_floor_num"] = "", ""
                # 装修
                try:
                    dic['decoration'] = html.xpath(
                        'string(//span[contains(text(), "装修：")]/following-sibling::*[1])').strip()
                except:
                    dic['decoration'] = ''
                # 用途
                try:
                    dic['usage'] = html.xpath(
                        'string(//span[contains(text(), "类型：")]/following-sibling::*[1])').strip()
                except:
                    dic['usage'] = ""
                # 楼盘名
                try:
                    dic["project_name"] = html.xpath(
                        'string(//node()[contains(text(), "小区：")]/following-sibling::a[1])').strip()
                except:
                    dic["project_name"] = ""

                # 行政区
                try:
                    area = html.xpath(
                        'string(//node()[contains(text(), "小区：")]/following-sibling::a[2])').strip()
                    if area:
                        dic["area"] = area
                except:
                    pass

                # 房屋配套
                try:
                    supporting_list = html.xpath(
                        '//ul[@class="house-info-peitao cf"]/li[contains(@class, "has")]/div/text()')
                    dic['supporting_facilities'] = "、".join(supporting_list)
                except Exception as e:
                    dic['supporting_facilities'] = ''

                # 联系电话
                try:
                    dic['tel'] = html.xpath("string(//span[@id='mobilecode'])")
                except Exception as e:
                    dic['tel'] = ''

                if not all([dic["project_name"], dic["case_happen_date"]]):
                    dic['d_status'] = 'err'
                    print(dic['project_name'],dic['case_happen_date'])
        else:
            dic['d_status'] = 'err'
            print('页面解析错误')

        # 补充字段
        dic['unitprice'] = ""
        dic['build_type'] = ""
        dic['house_structure'] = ""
        dic['affiliated_house'] = ""
        dic['usable_area'] = ""
        dic["build_date"] = ""
        dic['remaining_years'] = ""
        dic['new_ratio'] = ""
        dic['remark'] = ""
        dic['build_name'] = ""
        dic['house_name'] = ""
        dic['currency'] = "人民币"
        dic['case_type'] = "月平方米租报盘"
        print(dic)
        return dic
