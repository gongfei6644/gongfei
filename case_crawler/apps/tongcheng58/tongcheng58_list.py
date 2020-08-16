# coding=utf-8
import logging
from urllib.parse import urljoin

from lxml import etree
import re
import datetime

import traceback
from utils import common_tools

import requests

from utils.common_tools import get_rand_guid


def list_58tongcheng(logger, content, sub_info):
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
            items = content.xpath("//ul[@class='house-list-wrap']/li")
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:
                crt_time = datetime.datetime.now()
                case_date = crt_time.strftime("%Y%m")

                str_crt_time = crt_time.strftime("%Y-%m-%d %H:%M:%S")

                try:
                    title = item.xpath("./div[@class='list-info']/h2[@class='title']/a/text()")[0]
                    title = re.sub(re.compile(r'\s+'), "", title)
                    t_url = item.xpath(".//h2[@class='title']/a/@href")[0]
                    t_url = t_url if t_url.startswith("http") else urljoin(sub_info["sub_area_url"], t_url)
                    str_u_price = item.xpath("./div[@class='price']/p[@class='unit']/text()")[0]
                    u_price = re.findall('(\d+)', str_u_price)[0]  # 单价
                    if "万" in str_u_price:
                        u_price = float(u_price) * 10000
                    guid = get_rand_guid(t_url, u_price, case_date)
                except:
                    # 无效案例
                    logger.error("解析必要字段失败{}, 检查是否存在无效案例{}".format(traceback.format_exc(), sub_info["page_url"]))

                else:
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
                        baseinfo_list = item.xpath("./div[@class='list-info']/p[@class='baseinfo'][1]/span")
                        if len(baseinfo_list) > 0:
                            for baseinfo in baseinfo_list:
                                span_text = baseinfo.xpath("string(./text())")
                                if "室" in span_text:
                                    house_type = span_text  # 户型
                                if '㎡' in span_text or '平米' in span_text:
                                    house_area = re.findall('(\d+(\.\d+)?)', span_text)[0][0]  # 面积 120㎡
                                if '层' in span_text:
                                    floor_no = span_text  # 楼层 低层(共7层)
                                # 朝向
                                for flag in orientation_list:
                                    if flag in span_text:
                                        orientation = span_text
                                        break
                        # 拆分楼层和总楼层
                        if len(floor_no) > 0:
                            p_floor = floor_no
                            floor_no = re.findall("([低中高]{1}层)", p_floor)
                            if floor_no:
                                floor_no = floor_no[0]
                            else:
                                floor_no = ''
                            total_floor_num = re.findall("共(\d+)层", p_floor)
                            if total_floor_num:
                                total_floor_num = total_floor_num[0]
                            else:
                                total_floor_num = ''
                        str_t_price = item.xpath("./div[@class='price']/p[@class='sum']/b/text()")[0]  # 总价
                        t_price = re.findall('\d+', str_t_price)[0]  # 总价

                        p_list = item.xpath("./div[@class='list-info']/p[@class='baseinfo'][2]/span/a")  # 楼盘名称
                        if len(p_list) > 0:
                            plot_name = p_list[0].xpath("string(./text())")
                            plot_name = re.sub(re.compile(r'\s+'), "", plot_name)
                            address = ""
                            if len(p_list) >= 3:
                                address = p_list[2].xpath("string(./text())")
                                address = re.sub(re.compile(r'\s+'), "", address)
                        else:
                            plot_name, address = "", ""

                        dic_page = {"_id": guid,
                                    "city": sub_info["city"],
                                    "title": title,
                                    "source_link": t_url,
                                    "data_source": sub_info["source"],
                                    "crt_time": str_crt_time,
                                    "house_structure": house_structure,
                                    "project_alias": project_alias,
                                    "inside_space": inside_space,
                                    "usable_area": usable_area, "unitprice": u_price,
                                    "total_price": t_price,
                                    "address": address,
                                    "project_name": plot_name,
                                    "house_type": house_type,
                                    "house_area": house_area,
                                    "floor_no": floor_no,
                                    "total_floor_num": total_floor_num,
                                    "orientation": orientation,
                                    "build_date": build_date, "area": sub_info["area"],
                                    "sub_area": sub_info["sub_area"],
                                    "case_type_code": 3001001,
                                    "list_page_url": sub_info["page_url"]
                                    }
                    except Exception as e:
                        logger.error("解析页面异常{}{}, {}".format(e, traceback.format_exc(), sub_info["page_url"]))
                    else:
                        data_list.append(dic_page)

            try:
                next_href = content.xpath('string(//*[@class="next"]/@href)')
                if not next_href or not data_list:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页标签异常".format(sub_info["page_url"]))

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
