# coding=utf-8
import random
import re
import logging
import datetime
import time
import traceback
import requests
from lxml import etree
from urllib.parse import urljoin
from utils import common_tools
from utils.common_tools import get_rand_guid


def list_anjuke(logger, content, sub_info):
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
            items = content.xpath("//ul[@id='houselist-mod-new']/li")
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:
                house_structure = ""  # 户型（如：一室一厅，两室一厅，两室两厅）
                project_alias = ""  # 楼盘别名
                inside_space = ""  # 套内面积
                usable_area = ""  # 使用面积

                # 房屋信息
                house_type = ""  # 户型
                house_area = ""  # 面积
                floor_no = ""  # 楼层
                orientation = ""  # 朝向 安居客没有
                build_date = ""  # 建筑年代
                total_floor_num = ""  # 总楼层
                # 添加列表默认字段
                crt_time = datetime.datetime.now()  # 当前消息时间
                try:
                    title = item.xpath(
                        "./div[@class='house-details']/div[@class='house-title']/a/text()")[0].strip()  # 标题
                    detail_url = item.xpath(
                        "./div[@class='house-details']/div[@class='house-title']/a/@href")[0].strip()
                    detail_url = re.sub(r'&now_time=\d+', "", detail_url)
                    unit_price_str = item.xpath("./div[@class='pro-price']/span[@class='unit-price']/text()")[0]  # 单价
                    unit_price = re.findall(r'\d+\.?\d*', unit_price_str)[0]
                    if "万" in unit_price_str:
                        unit_price = float(unit_price) * 10000
                except:
                    pass  # 无效案例
                else:
                    try:
                        props = item.xpath("string(.//div[@class='details-item'])")
                        # 户型（如：一室一厅，两室一厅，两室两厅）
                        house_type = re.findall("(\d室.*?)\|", props)
                        if house_type:
                            house_type = house_type[0]

                        # 建筑面积(案例的面积)
                        try:
                            house_area = re.findall("(\d+)m²", props)
                            if house_area:
                                house_area = house_area[0]

                        except Exception as err:
                            house_area = ""

                        if len(house_area) == 0:
                            msg = "关键字段缺失，{}".format(sub_info)
                            logger.info(msg)

                        # 楼层
                        floor_no = re.findall("([低中高]{1}层)", props)
                        if floor_no:
                            floor_no = floor_no[0]
                        else:
                            floor_no = ''
                        # 总层数
                        total_floor_num = re.findall("共(\d+)层", props)
                        if total_floor_num:
                            total_floor_num = total_floor_num[0]
                        else:
                            total_floor_num = ''
                        # 建筑年代
                        build_date = re.findall("(\d{4})年建", props)
                        if build_date:
                            build_date = build_date[0]
                        else:
                            build_date = ''
                    except Exception as error:
                        msg = "住宅信息获取失败，{},错误信息：{}".format(sub_info, error)
                        logger.error(msg)

                    project_name = ''
                    address = ''
                    try:
                        address_section = item.xpath(".//span[@class='comm-address']/@title")
                        if address_section:
                            address_section = address_section[0].strip()
                            address_section = re.sub("\s+", ' ', address_section)
                            # print("address_section",address_section)
                            # 项目名称
                            # try:
                            #     pro_name = address_section.split(' ')
                            #     # print("pro_name",pro_name)
                            #     if pro_name:
                            #         project_name = pro_name[0]
                            # except Exception as e:
                            #     print(e)
                            #
                            # if len(project_name) == 0:
                            #     msg = "关键字段缺失，没有找到楼盘名称,{}".format(sub_info)
                            #     logger.info(msg)

                            # 地址
                            address = address_section.split(' ')[1].split('-')
                            if len(address) == 3:
                                address = address[2]
                            else:
                                address = ''
                    except Exception as error:
                        msg = "楼盘名称和地址信息获取失败：{},错误信息：{}{}".format(
                            sub_info["sub_area_url"], error, traceback.format_exc())
                        logger.error(msg)

                    try:
                        str_t_price = item.xpath(
                            "./div[@class='pro-price']/span[@class='price-det']/strong/text()")[0]  # 总价
                    except Exception as error:
                        t_price = ''
                        msg = "总价信息获取失败，{},错误信息：{}".format(sub_info["sub_area_url"], traceback.format_exc())
                        logger.error(msg)
                    else:
                        t_price = re.findall('\d+', str_t_price)[0]  # 总价

                    try:
                        case_date = crt_time.strftime("%Y%m")
                        guid = get_rand_guid(detail_url.split("?")[0], unit_price, case_date)
                        cityname = common_tools.check_cityname(sub_info["city"])
                        dic_page = {"_id": guid,
                                    "city": cityname,
                                    "title": title,
                                    "source_link": detail_url,
                                    "data_source": sub_info["source"],
                                    "crt_time": str(crt_time),
                                    "house_structure": house_structure,
                                    "project_alias": project_alias,
                                    "inside_space": inside_space,
                                    "usable_area": usable_area,
                                    "unitprice": unit_price,
                                    "total_price": t_price,
                                    "address": address,
                                    # "project_name": project_name,
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

                    except:
                        print(traceback.print_exc())
                    else:
                        data_list.append(dic_page)

            try:
                next_href = content.xpath("string(//a[contains(text(),'下一页')]/@href)")
                if not next_href or not data_list:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))

    dic_data = {"data": data_list, "flag": flag}
    return dic_data


if __name__ == '__main__':
    url = "http://xm.ershoufang.zhuge.com/wuyuanwan/"
    headers = {'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
               'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)',
               }
    resp = requests.get(
        url,
        headers=headers)
    content = etree.HTML(resp.content.decode("utf-8"))
    html_str = {"str": resp.content.decode("utf-8")}
    logger = logging.getLogger("")
