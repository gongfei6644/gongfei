from lxml import etree
import datetime
import time
import requests
import json
import re
import bs4

from utils.common_tools import format_num


class ParseLianJ:

    def parse_xpath(self, html_str):

        dic = {}
        now_time = datetime.datetime.now()
        dic['detail_time'] = now_time.strftime('%Y-%m-%d %H:%M:%S')
        if html_str['str'] == '404':
            dic['d_status'] = 0
            return dic
        elif html_str['str']:
            html = etree.HTML(html_str['str'])
            # 租金
            try:
                # price_info = html.xpath('string(//p[@class="content__aside--title"])').strip()
                price_info = html.xpath('string(//div[@class="content__aside--title"])').strip()
                total_price = re.findall(r'\d+.*元/月', price_info, re.S)
                dic['total_price'] = total_price[0].strip() if total_price else ""
                deposit_method_info = html.xpath('string(.//span[contains(text(),"租赁方式：")]/parent::li)')
                # deposit_method = re.findall(r'\((.+)\)', price_info)
                # dic['deposit_method'] = deposit_method[0] if deposit_method else ""
                deposit_method = re.findall(r'租赁方式：(.*)', deposit_method_info)
                dic['deposit_method'] = deposit_method[0] if deposit_method else ""
            except:
                dic['total_price'], dic['deposit_method'] = "", ""
            # 案例时间
            try:
                happen_date = html.xpath('//div[@class="content__subtitle"]/text()')
                dic['case_happen_date'] = re.sub(r'\s+', '', "".join(happen_date)).strip("房源上架时间").strip('房源维护时间：')
            except:
                dic['case_happen_date'] = ""
            try:
                # central_heating = html.xpath('string(//i[@data-class="central_heating"])')
                central_heating = html.xpath('string(//li[contains(text(),"采暖：")])').split('：')[1]
            except:
                central_heating = ""

            try:
                dic['usage'] = html.xpath('string(//i[@data-class="authorization_apartment"]/text())')
            except:
                dic['usage'] = ""
            try:
                dic['remark'] = html.xpath('string(//i[@class="content__item__tag--only_woman"]/text())')
            except:
                dic['remark'] = ""
            try:
                dic['decoration'] = html.xpath('string(//i[@class="content__item__tag--decoration"]/text())')
            except:
                dic['decoration'] = ""
            try:
                # dic['house_type'] = html.xpath('string(//i[@class="typ"]/parent::span[1]/text())')
                house_type = html.xpath('string(.//span[contains(text(),"房屋类型：")]/parent::li)').split(' ')[0].split('：')[1]
                dic['house_type'] = house_type
            except:
                dic['house_type'] = ""
            try:
                # build_area = html.xpath('string(//i[@class="area"]/parent::span[1]/text())')
                build_area = html.xpath('string(.//li[contains(text(),"面积：")])')
                dic['build_area'] = format_num(build_area.split('：')[1])
            except:
                dic['build_area'] = ""
            try:
                # dic['orientation'] = html.xpath('string(//i[@class="orient"]/parent::span[1]/text())').strip("朝 ")
                # dic['orientation'] = "" if " " in dic['orientation'] else dic['orientation']
                orientation = html.xpath('string(.//span[contains(text(),"朝向楼层：")]/parent::li)').split(' ')[0].split('：')[1]
                dic['orientation'] = orientation.replace('/','')
            except:
                dic['orientation'] = ""

            try:
                dic['lease_period'] = html.xpath('string(//li[contains(text(), "租期")]/text())').strip("租期：")
            except:
                dic['lease_period'] = ""
            try:
                floor_info = html.xpath('string(//li[contains(text(), "楼层：")]/text())').replace("楼层：", "")
                total_floor = re.findall(r'(\d+)层', floor_info)
                dic['total_floor_num'] = total_floor[0] if total_floor else ""
                dic['floor_no'] = floor_info.split("/")[0].replace("楼", "")

            except:
                dic['floor_no'], dic['total_floor_num'] = "", ""
            try:
                # dic['rental_method'] = html.xpath('string(//i[@class="house"]/parent::span[1]/text())')  # 租期
                dic['rental_method'] = html.xpath('string(//li[contains(text(),"租期：")])').replace("租期：","") # 租期

            except:
                dic['rental_method'] = ""

            try:
                is_elevator = html.xpath('')
            except:
                is_elevator = ""
            try:
                supporting = html.xpath(
                    '//li[text()="配套设施"]/following-sibling::li[not(contains(@class, "_no"))]/text()')
                supporting = [i.strip() for i in supporting if i]
            except:
                supporting = []
            if central_heating == "集中供暖":
                supporting.append("集中供暖")
            if is_elevator == "有":
                supporting.append("电梯")
            supporting = [i for i in supporting if i]
            dic['supporting_facilities'] = "、".join(supporting)
            try:
                dic['tel'] = html.xpath('string(//span[@data-el="updatePhone"]/text())')
            except:
                dic['tel'] = ""

            if dic['case_happen_date']:
                dic['d_status'] = 1
            else:
                dic['d_status'] = 'err'
        else:
            dic['d_status'] = 'err'

        # 补充字段
        dic['build_type'] = ""
        dic['house_structure'] = ""
        dic['affiliated_house'] = ""
        dic['usable_area'] = ""
        dic["build_date"] = ""
        dic['remaining_years'] = ""
        dic['new_ratio'] = ""
        dic['build_name'] = ""
        dic['house_name'] = ""
        dic['unitprice'] = ""
        dic['currency'] = "人民币"
        dic['case_type'] = "月平方米租报盘"
        print(dic)
        return dic
