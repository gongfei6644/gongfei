# coding=utf-8
import logging

from lxml import etree
import re
import datetime

import traceback
from utils import common_tools

import requests


def list_zhugezhaofang(logger, content, sub_info):
    """
    解析诸葛找房二手房
    :param logger: 日志管理器
    :param content: 下载其返回对象
    :param sub_info: 片区信息
    :return:
    """
    logger.info("进入解析函数,{}".format(sub_info["page_url"]))
    data_list = []
    flag = "normal"
    if content == "404":
        flag = "finish"

    elif content == "retry":
        flag = "normal"
    else:
        try:
            expired = content.xpath('//div[@class="null-house-box"]')
            if expired:
                flag = "finish"
                items = None
            else:
                items = content.xpath('//ul[@id="listTableBox"]/li')
        except Exception as e:
            items = None
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))

        if items is not None:
            for item in items:
                dic = {}
                crt_time = datetime.datetime.now()  # 当前消息时间
                try:
                    title = item.xpath('.//div[@class="title"]/a/@title')[0]  # 标题
                    detail_url = item.xpath('.//div[@class="title"]/a/@href')[0]  # 详情链接
                    unit_price = item.xpath('.//strong/text()')[0]  # 单价
                    unit_price = re.findall(r'\d+\.?\d*', unit_price)[0]
                except:
                    logger.error("检查是否存在无效到案例{}".format(sub_info["page_url"]))
                else:
                    try:
                        info_list = item.xpath('./span[@class="list-table-info-box"]/span[2]/text()')
                        info = re.sub('\s', "", "".join(info_list))
                    except:
                        house_area, floor_no, house_type, build_date, orientation = "", "", "", "", ""
                    else:
                        try:
                            house_area = re.findall(r'(\d+\.?\d*)m²', info)[0]  # 建筑面积
                        except:
                            house_area = ""
                        try:
                            house_type = re.findall(r'(\d*室\d*厅?)', info)[0]  # 户型
                        except:
                            house_type = ""
                        try:
                            floor_no = re.findall(r'([高中低]楼层)', info)[0].replace("楼", "")  # 楼层
                        except:
                            floor_no = ""
                        try:
                            build_date = re.findall(r'(\d+年建)', info)[0]  # 建筑年代
                        except:
                            build_date = ""
                        try:
                            orientation = re.findall(r'\|([东南西北]+)', info)[0]  # 朝向
                        except:
                            orientation = ""
                    try:
                        total_price = item.xpath('string(.//b/text())')  # 总价
                    except:
                        total_price = ""
                    try:
                        area_list = item.xpath('.//span[@class="list-table-info-box"]/span[1]//text()')
                        area_str = re.sub('\s', "", "".join(area_list))
                    except:
                        project_name, address = "", ""
                    else:
                        try:
                            address = re.findall(r'\](.*$)', area_str)[0]
                        except:
                            address = ""
                    try:
                        dic["case_type_code"] = 3001001
                        dic["list_page_url"] = sub_info["page_url"]
                        dic["data_source"] = sub_info["source"]
                        dic["city"] = sub_info["city"]
                        dic["crt_time"] = crt_time.strftime("%Y-%m-%d %H:%M:%S")
                        dic["title"] = title
                        dic["source_link"] = detail_url
                        dic["unitprice"] = unit_price
                        dic["house_area"] = house_area
                        dic["unitprice"] = unit_price
                        # dic["project_name"] = project_name
                        dic["total_price"] = total_price
                        dic["house_type"] = house_type
                        dic["floor_no"] = floor_no
                        dic["build_date"] = build_date
                        dic["orientation"] = orientation
                        dic["area"] = sub_info["area"]
                        dic["sub_area"] = sub_info["sub_area"]
                        dic["address"] = address
                        case_date = crt_time.strftime("%Y%m")
                        dic["_id"] = common_tools.get_rand_guid(detail_url, unit_price, case_date)
                    except:
                        print(traceback.print_exc())
                    else:
                        data_list.append(dic)

            # 判断是否尊在下一页
            try:
                next_href = content.xpath('string(//a[@class="laypage-next"]/@href)')
                if not next_href or not data_list:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))

    dic_data = {"data": data_list, "flag": flag}
    return dic_data


if __name__ == '__main__':
    list_zhugezhaofang("", "", "")
