# coding=utf-8

import re
import logging
import datetime
import traceback
import requests
from lxml import etree
from urllib.parse import urljoin
from utils import common_tools


def list_fangchanchaoshi(logger, content, sub_info):
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
            items = content.xpath("//div[@class='fy_list']/ul/li[@class='item salelist']")
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:
                dic = {}
                # 添加列表默认字段
                crt_time = datetime.datetime.now()  # 当前消息时间
                str_crt_time = crt_time.strftime("%Y-%m-%d %H:%M:%S")
                house_structure = ""  # 户型（如：一室一厅，两室一厅，两室两厅）
                project_alias = ""  # 楼盘别名
                inside_space = ""  # 套内面积
                usable_area = ""  # 使用面积

                # 房屋信息
                house_type = ""  # 户型
                house_area = ""  # 面积
                floor_no = ""  # 楼层
                orientation = ""  # 朝向
                build_date = ""  # 建筑年代
                total_floor_num = ""  # 总楼层
                orientation_list = ['东', '南', '西', '北']
                try:
                    title = item.xpath("./div[@class='info0']//div[@class='t_1 fl']/text()")[0]
                    title = re.sub(re.compile(r'\s+'), "", title)
                    t_url = item.xpath("./div[@class='info0']/div[@class='t']/a/@href")[0]
                    t_url = t_url if sub_info["sub_area_url"].startswith("http") else urljoin(
                        sub_info["sub_area_url"], t_url)
                    str_u_price = item.xpath(".//div[@class='p2 tr']/text()")[0]  # 建面单价
                    u_price = re.findall('(\d+)', str_u_price)[0]  # 单价
                except:
                    # 无效案例
                    title, t_url, u_price = "", "", ""
                    logger.info("检查无效案例{}".format(sub_info["page_url"]))

                else:
                    try:
                        plot_name = ""  # 楼盘名称
                        address = ""  # 楼盘地址
                        plot_name = item.xpath(".//div[@class='lp']/label[@class='f14 fb']/a/text()")[0]  # 楼盘名称
                        address = item.xpath(".//div[@class='lp']/label[2]/text()")[0]  # 楼盘地址 网页格式 [宝安-] 宝民一路
                        address = re.sub(r'\[.*\]', "", address, count=0)  # 变为 宝民一路

                        houseInfo_desc = item.xpath("string(.//div[@class='s']/label)").replace("\r\n", "").replace(" ",
                                                                                                                    "")
                        houseInfo_list = houseInfo_desc.split('|')

                        usage = ""  # 用途
                        if len(houseInfo_list) > 0:
                            for houseinfo in houseInfo_list:
                                if "室" in houseinfo:
                                    house_type = houseinfo  # 户型
                                # 朝向
                                for fflag in orientation_list:
                                    if fflag in houseinfo:
                                        orientation = houseinfo
                                        break
                                if "公寓" in houseinfo or "住宅" in houseinfo:
                                    usage = houseinfo  # 用途
                                if '层' in houseinfo:
                                    floor_no = houseinfo  # 楼层 14/29层
                                    # 拆分楼层和总楼层
                                    try:
                                        if len(floor_no) > 0:
                                            p_floor = floor_no  # "14/29层"
                                            floor_group = re.findall("\d+", p_floor)
                                            if len(floor_group) == 2:
                                                floor_no = str(floor_group[0])
                                                total_floor_num = str(floor_group[1])
                                            else:
                                                floor_no = re.findall("[高中低]层", p_floor)[0]
                                                total_floor_num = str(floor_group[0])
                                    except Exception as e:
                                        floor_no, total_floor_num = "", ""
                                        logger.error("解析楼层数据异常: {}{}".format(e, traceback.format_exc()))

                                if '年建' in houseinfo:
                                    build_date = re.findall("(\d+)年建", houseinfo)
                                    if build_date:
                                        build_date = build_date[0]
                                    else:
                                        build_date = ""
                        # 面积
                        area_info = item.xpath(".//div[@class='p1']/div[@class='fl']/text()")[0]
                        house_area = re.findall('(\d+(\.\d+)?)', area_info)[0][0]  # 面积 120㎡

                        # 建面单价和总价
                        str_t_price = item.xpath("string(.//div[@class='p1']/div[@class='fr w_c_1 fb']/span/text())")  # 总价
                        t_price = re.findall('\d+', str_t_price)[0]  # 总价

                        # 获取随机guid
                        case_date = crt_time.strftime("%Y%m")
                        guid = common_tools.get_rand_guid(t_url, u_price, case_date)  # id 用单价和链接+当前月份
                        cityname = common_tools.check_cityname(sub_info["city"])
                        # 建筑结构
                        building_structure = item.xpath(
                            "string(.//div[@class='s1']/div[@class='fl tag']/text())")  # 建筑结构
                        dic_page = {"_id": guid, "city": cityname,
                                    "title": title,
                                    "source_link": t_url,
                                    "data_source": sub_info["source"],
                                    "crt_time": str_crt_time,
                                    "house_structure": house_structure,
                                    "project_alias": project_alias,
                                    "inside_space": inside_space,
                                    "usable_area": usable_area,
                                    "unitprice": u_price,
                                    "total_price": t_price,
                                    "address": address, "project_name": plot_name,
                                    "house_type": house_type, "house_area": house_area,
                                    "floor_no": floor_no,
                                    "total_floor_num": total_floor_num,
                                    "orientation": orientation,
                                    "build_date": build_date,
                                    "area": sub_info["area"],
                                    "sub_area": sub_info["sub_area"],
                                    "case_type_code": 3001001,
                                    "list_page_url": sub_info["page_url"],
                                    "usage": usage,
                                    "building_structure": building_structure
                                    }
                        data_list.append(dic_page)
                    except Exception as e:
                        logger.error("解析数据异常{},{}".format(e, traceback.format_exc()))
            try:
                next_href = content.xpath('string(//*[contains(text(),"下一页")]/@href)')
                if not next_href or not data_list:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except Exception as e:
                logger.info("解析下一页异常{}, {}".format(e, sub_info["page_url"]))
    dic_data = {"data": data_list, "flag": flag}
    return dic_data


if __name__ == '__main__':
    url = "http://xm.ershoufang.zhuge.com/wuyuanwan/"
    headers = {'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
               'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)',
               }
    resp = requests.get(url,  headers=headers)
    content = etree.HTML(resp.content.decode("utf-8"))
    html_str = {"str": resp.content.decode("utf-8")}
    logger = logging.getLogger("")
