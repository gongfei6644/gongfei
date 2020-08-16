# coding=utf-8
import logging
from urllib.parse import urljoin

from lxml import etree
import re
import datetime

import traceback
from utils import common_tools

import requests

from utils.common_tools import get_full_url, format_num
from utils.constants import PATTTERN_MAP


def list_lianjia(logger, content, sub_info):
    """"
    解析诸葛找房租房
    """
    logger.info("进入解析函数,{}".format(sub_info["page_url"]))
    data_list = []
    flag = "normal"
    if content == "404":
        flag = "finish"

    elif content == "retry":
        flag = "normal"
    else:
        html = etree.HTML(content)
        try:
            items = html.xpath('//div[@class="content__list"]/div[@class="content__list--item"]')
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:
                crt_time = datetime.datetime.now()  # 当前消息时间
                str_crt_time = crt_time.strftime("%Y-%m-%d %H:%M:%S")

                try:
                    title = item.xpath('.//p[@class="content__list--item--title twoline"]/a/text()')[0].strip()  # 标题
                    detail_href = item.xpath('.//p[@class="content__list--item--title twoline"]/a/@href')[0]
                    detail_url = get_full_url(sub_info["sub_area_url"], detail_href)
                    total_price = item.xpath('.//span[@class="content__list--item-price"]//text()')[0]  # 租金
                    total_price = format_num(total_price)
                    area = item.xpath('.//p[@class="content__list--item--des"]/a[1]/text()')[0].strip()
                except:
                    # 无效案例
                    title, detail_url, total_price,area = '', '', '',''
                if all([title, detail_url, total_price]):
                    try:
                        rental_method = title.split("·")[0]
                        project_name = title.split("·")[1].split(" ")[0]
                    except Exception as e:
                        rental_method, project_name = "", ""
                        logger.error("解析小区名异常: {}, {}".format(e, traceback.format_exc()))

                    case_date = crt_time.strftime("%Y%m")
                    uid = common_tools.get_rand_guid(detail_url, total_price, case_date)  # id 用单价和链接+当前月份

                    dic_item = {"_id": uid,
                                "crt_time": str_crt_time,
                                "data_source": sub_info["source"],
                                "city": sub_info["city"],
                                # "area": sub_info["area"],
                                "area": area,
                                "sub_area": sub_info["sub_area"],
                                "list_page_url": sub_info["page_url"],
                                "title": title,
                                "source_link": detail_url,
                                "rental_method": rental_method,
                                "project_name": project_name,
                                }
                    data_list.append(dic_item)
            try:
                cur_page = html.xpath('//div[@class="content__pg"]/@data-curpage')
                total_page = html.xpath('//div[@class="content__pg"]/@data-totalpage')
                next = check_page(cur_page, total_page)
                if not all([next, data_list]):
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))

    dic_data = {"data": data_list, "flag": flag}
    print(dic_data)
    return dic_data


def check_page(cur_page, total_page):
    result = False
    try:
        if int(cur_page) < int(total_page):
            result = True
    except:
        pass
    return result
