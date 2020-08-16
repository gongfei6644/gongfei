# coding=utf-8

import re
import logging
import datetime
import traceback
import requests
from lxml import etree
from urllib.parse import urljoin
from utils import common_tools


def list_qfang(logger, content, sub_info):
    """"
    解析q房网二手房
    """
    data_list = []
    flag = "normal"
    if content == "404":
        flag = "finish"

    elif content == "retry":
        flag = "retry"
    else:
        try:
            items = content.xpath("//div[@id='cycleListings']/ul/li[@class='clearfix']")

        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:
                dic = {}
                # 添加列表默认字段
                crt_time = datetime.datetime.now()  # 当前消息时间
                try:
                    title = item.xpath('string(.//a[@key="showKeyword"]/@title)').strip()  # 标题
                    detail_href = item.xpath(
                        'string(.//a[@key="showKeyword"]/@href)')  # /ershoufang/gzhz0002209561.html
                    detail_url = urljoin(sub_info["sub_area_url"], detail_href)
                    unit_price = item.xpath('string(.//div[@class="show-price"]/p/text())')  # 单价
                    unit_price = re.findall(r'\d+\.?\d*', unit_price)[0]

                except:
                    # 无效案例
                    pass

                else:
                    try:
                        info_list = item.xpath('.//p[@class="house-about clearfix"]//text()')
                        info = re.sub('\s', "", "".join(info_list))  # 2室2厅61.35平米普通装修高层/33层北2011年建
                    except:
                        house_area, house_type, floor_no, total_floor_num, orientation, build_date = "", "", "", "", "", ""
                    else:
                        try:
                            house_area = re.findall(r'(\d+\.?\d*)平米', info)[0]  # 建筑面积
                        except:
                            house_area = ""
                        try:
                            house_type = re.findall(r'(\d*室\d*厅)', info)[0]  # 户型
                        except:
                            house_type = ""

                        try:
                            floor_no = re.findall(r'([高中低]层)', info)[0]
                        except:
                            floor_no = ""
                        try:
                            total_floor_num = re.findall(r'(\d+)层', info)[0]
                        except:
                            total_floor_num = ""
                        try:
                            orientation = re.findall(r'[东南西北]+', info)[0]  # 朝向
                        except:
                            orientation = ""
                        try:
                            build_date = re.findall(r'\d+年建', info)[0]  # 建筑年代
                        except:
                            build_date = ""
                    try:
                        total_price = item.xpath('string(.//span[@class="sale-price"]/text())').strip()  # 总价
                    except:
                        total_price = ""

                    try:
                        project_info = item.xpath('string(.//span[@class="whole-line"]/a[3]/text())').strip()  # 楼盘
                        project_alias_list = re.findall(r'\((.+)\)', project_info)
                        if project_alias_list:
                            project_alias = project_alias_list[0]
                            project_name = project_info.split("(")[0]
                        else:
                            project_alias = ""
                            project_name = project_info

                    except:
                        project_alias, project_name = "", ""

                    try:
                        case_date = crt_time.strftime("%Y%m")
                        dic["_id"] = common_tools.get_rand_guid(detail_url, unit_price, case_date)
                        dic["case_type_code"] = 3001001
                        dic["data_source"] = sub_info["source"]
                        dic["city"] = common_tools.check_cityname(sub_info["city"])  # 返回标准城市名称
                        dic["area"] = sub_info["area"]
                        dic["sub_area"] = sub_info["sub_area"]
                        dic["crt_time"] = crt_time.strftime("%Y-%m-%d %H:%M:%S")
                        dic["title"] = title
                        dic["source_link"] = detail_url.strip()
                        dic["unitprice"] = unit_price
                        dic["house_area"] = house_area
                        dic["unitprice"] = unit_price
                        dic["project_name"] = project_name  # 小区/楼盘
                        dic["project_alias"] = project_alias  # 楼盘别名
                        dic["total_price"] = total_price
                        dic["house_type"] = house_type
                        dic["floor_no"] = floor_no
                        dic["build_date"] = build_date
                        dic["orientation"] = orientation  # 朝向
                        dic["total_floor_num"] = total_floor_num
                    except:
                        print(traceback.print_exc())
                    else:

                        data_list.append(dic)
            try:
                next_href = content.xpath('string(//a[@class="turnpage_next"])')

                if not all([next_href, data_list]):
                    flag = "finish"
                    logger.info("{}没有下一页".format(sub_info["page_url"]))
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
