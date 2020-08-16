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
        now_time = datetime.datetime.now()
        dic['detail_time'] = now_time.strftime('%Y-%m-%d %H:%M:%S')

        if html_str['str'] == '404':
            dic['d_status'] = 0
            return dic
        elif html_str['str'] == '访问页面不存在':
            dic['d_status'] = "Page missing"
            return dic
        elif html_str['str']:
            text = html_str['str'].replace('&nbsp;', '')
            html = etree.HTML(text)
            try:
                node = html.xpath('//div[@class="tab-cont-right"]')[0]
            except:
                dic['d_status'] = 'err'
                return dic
            else:
                # 案例时间
                try:
                    dic['case_happen_date'] = html.xpath('string(//span[contains(text(), "更新时间")])').strip("更新时间 ")
                except:
                    dic['case_happen_date'] = ""
                # 楼盘名
                try:
                    pn1 = node.xpath('string(.//div[text()="小区"]/following-sibling::*[1]/a)').strip()
                    pn2 = node.xpath('string(//div[@class="tr-line"]/div[1]/div[2])').strip()
                    dic['project_name'] = pn1 or pn2

                except:
                    dic['project_name'] = html.xpath('string(//div[@class="bread"]/a[last()])').replace("租房", "")
                try:
                    price_info = node.xpath('string(//div[contains(@class,"trl-item sty1")])')
                    dic['total_price'] = price_info.split("（")[0].strip()
                except:
                    dic['total_price'] = ""
                # 押金方式
                try:
                    deposit_info = node.xpath('string(//div[contains(@class,"trl-item sty1")])')
                    deposit_method = re.findall(r'（(.+)）', deposit_info, re.S)
                    dic["deposit_method"] = deposit_method[0]
                except:
                    dic["deposit_method"] = ""
                # print("案例总价", dic["total_price"],"押付方式",dic["deposit_method"])
                # 出租方式
                try:
                    dic['rental_method'] = node.xpath('string(.//div[text()="出租方式"]/preceding-sibling::*[1])').strip()
                except:
                    dic['rental_method'] = ""
                # 户型
                try:
                    dic['house_type'] = node.xpath('string(.//div[text()="户型"]/preceding-sibling::*[1])').strip()
                except:
                    dic['house_type'] = ""
                # 建筑面积
                try:
                    build_area = node.xpath('string(.//div[text()="建筑面积"]/preceding-sibling::div[1])').strip("平米 ")
                    dic['build_area'] = float(build_area) if build_area else ""
                except:
                    dic['build_area'] = ""
                # 朝向
                try:
                    dic['orientation'] = node.xpath('string(.//div[text()="朝向"]/preceding-sibling::*[1])').strip()
                except:
                    dic['orientation'] = ""
                # 装修
                try:
                    dic['decoration'] = node.xpath('string(.//div[text()="装修"]/preceding-sibling::*[1])').strip()
                except:
                    dic['decoration'] = ""
                # 所在楼层
                try:
                    dic['floor_no'] = node.xpath(
                        'string(.//div[contains(text(), "楼层")]/preceding-sibling::*[1])').strip()
                except:
                    dic['floor_no'] = ""
                # 总楼层
                try:
                    total_floor = node.xpath('string(.//div[contains(text(), "楼层")])')
                    dic['total_floor_num'] = re.findall(r'\d+', total_floor)[0]
                except:
                    dic['total_floor'] = ""

                # 行政区
                try:
                    area = node.xpath('string(.//div[text()="小区"]/following-sibling::*[1])').strip()
                    if area:
                        area_ = re.findall(r'[(（](.*?)[）)]', area)[0].split('/')[0].strip()
                        dic['area'] = area_
                except:
                    pass

                # 地址
                try:
                    dic['address'] = node.xpath('string(.//div[text()="地址"]/following-sibling::*[1]/a)').strip()
                except:
                    dic['address'] = ""
                # 电话
                try:
                    dic['tel'] = node.xpath('string(.//p[@class="text_phone"])').strip()
                except:
                    dic['tel'] = ""
                # 配套
                try:
                    supporting_list = html.xpath('//div[text()="配套设施"]/following-sibling::div[1]//li/text()')
                    dic['supporting_facilities'] = "、".join(supporting_list)
                except Exception as e:
                    dic['supporting_facilities'] = ''

            if dic['project_name'] and dic['case_happen_date']:
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
        dic['remark'] = ""
        dic['build_name'] = ""
        dic['house_name'] = ""
        dic['unitprice'] = ""
        dic['currency'] = "人民币"
        dic['case_type'] = "月平方米租报盘"
        print(dic)
        return dic
