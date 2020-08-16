# coding=utf-8
import logging
from urllib.parse import urljoin

from lxml import etree
import re
import datetime

import traceback
from utils import common_tools

import requests

from utils.constants import PATTTERN_MAP


def list_lianjia(logger, content, sub_info):
    """"
    解析诸葛找房二手房
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
            items = content.xpath('//li[contains(@class, "LOGCLICKDATA")] | //li[contains(@class,"xiaoquListItem")]')
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:
                crt_time = datetime.datetime.now()  # 当前消息时间
                str_crt_time = crt_time.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    title = item.xpath("./div[@class='info clear']/div[@class='title']/a/text()")[0]  # 标题
                    title = re.sub(r'\s+', "", title)
                    t_url = item.xpath("./div[@class='info clear']/div[@class='title']/a/@href")[0]
                    t_url = t_url if t_url.startswith("http") else urljoin(sub_info["sub_area_url"], t_url)
                    str_u_price = item.xpath(".//div[@class='unitPrice']/span/text()")[0]  # 单价
                    u_price = re.findall(r'\d+\.?\d*', str_u_price)[0]
                    if "万" in str_u_price:
                        u_price = float(u_price) * 10000
                except:
                    # 无效案例
                    logger.error(
                        "无效案例{}".format(traceback.format_exc(), sub_info["page_url"]))

                else:
                    try:
                        houseInfo_desc = item.xpath(".//div[@class='houseInfo']/text()")
                        houseinfo = re.sub(r'\s', '', "".join(houseInfo_desc))
                    except:
                        house_type, house_area, orientation = "", "", ""
                    else:
                        try:
                            house_type = re.findall(r'\d*室\d*厅?\d*卫?', houseinfo)[0]
                        except:
                            house_type = ""
                        try:
                            house_area = re.findall(r'(\d+\.?\d*)平米', houseinfo)[0]  # 面积 120㎡
                        except:
                            house_area = ""
                        try:
                            orientation = re.findall(r'[东西南北]+', houseinfo)[0]
                        except:
                            orientation = ""
                    try:
                        positionInfo = item.xpath(".//div[@class='positionInfo']/text()")
                        positionInfo = re.sub(r'\s', "", "".join(positionInfo))
                    except:
                        floor_no, total_floor_num, build_date = "", "", ""
                    else:
                        try:
                            floor_info = PATTTERN_MAP["floor"].findall(positionInfo.replace("楼", ""))[0]
                            floor_no, total_floor_num = floor_info
                        except:
                            floor_no, total_floor_num = "", ""
                        try:
                            build_date = re.findall(r'(\d+)年建', positionInfo)[0]
                        except:
                            build_date = ""
                    try:
                        str_t_price = item.xpath(".//div[@class='totalPrice']/span/text()")[0]  # 总价
                        t_price = re.findall('\d+', str_t_price)[0]  # 总价
                    except:
                        t_price = ""

                    case_date = crt_time.strftime("%Y%m")
                    guid = common_tools.get_rand_guid(t_url, u_price, case_date)  # id 用单价和链接+当前月份
                    address = ""  # 楼盘地址
                    dic_page = {"_id": guid, "city": sub_info["city"],
                                "title": title, "source_link": t_url,
                                "data_source": sub_info["source"],
                                "crt_time": str_crt_time,
                                "unitprice": u_price,
                                "total_price": t_price,
                                "address": address,
                                "house_type": house_type,
                                "house_area": house_area,
                                "floor_no": floor_no,
                                "total_floor_num": total_floor_num,
                                "orientation": orientation,
                                "build_date": build_date,
                                "area": sub_info["area"],
                                "sub_area": sub_info["sub_area"],
                                "case_type_code": 3001001,
                                "list_page_url": sub_info["page_url"],
                                }
                    data_list.append(dic_page)
            try:
                next_href = content.xpath("string(//div[@class='page-box house-lst-page-box']/@page-url)")
                if not next_href or not data_list:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))

    dic_data = {"data": data_list, "flag": flag}
    return dic_data


