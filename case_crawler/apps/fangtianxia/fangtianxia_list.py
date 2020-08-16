# coding=utf-8
import logging
from urllib.parse import urljoin

from lxml import etree
import re
import datetime

import traceback
from utils import common_tools

import requests


def list_fangtianxia(logger, content, sub_info):
    """"
    解析房天下二手房
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
            items = content.xpath("//div[@class='shop_list shop_list_4']/dl[contains(@dataflag,'bg')]")
        except Exception as e:
            logger.error("解析案例节点异常:{},{}".format(e, sub_info["page_url"]))
        else:
            for item in items:
                crt_time = datetime.datetime.now()  # 当前消息时间
                try:
                    title = item.xpath(".//dd/h4/a/@title")[0]  # 标题
                    detail_url = item.xpath(".//dd/h4/a/@href")[0]  # 详情链接
                    channel = item.xpath("string(.//dd/h4/a/@data_channel)")
                    psid = item.xpath("string(.//dd/h4/a/@ps)")
                    t_url = detail_url if detail_url.startswith("http") else urljoin(sub_info["page_url"], detail_url)
                    # if all([channel, psid, "psid" not in t_url]):
                    #     t_url = t_url + "?channel={}&psid={}".format(channel, psid)
                    str_u_price = item.xpath(".//dd[@class='price_right']/span[2]/text()")[0].strip()  # 单价
                    u_price = re.findall(r'\d+\.?\d*', str_u_price)[0]
                    if "万" in str_u_price:
                        u_price = float(u_price) * 10000
                except:
                    # 无效案例
                    logger.error("检查无效案例{}".format(sub_info["page_url"]))
                else:
                    house_structure = ""  # 户型（如：一室一厅，两室一厅，两室两厅）
                    project_alias = ""  # 楼盘别名
                    inside_space = ""  # 套内面积f
                    usable_area = ""  # 使用面积
                    try:
                        str_t_price = item.xpath("string(.//dd[@class='price_right']/span[1])")
                        t_price = re.findall('\d+', str_t_price)[0]  # 总价

                        if "万" not in str_t_price:
                            t_price = float(t_price) / 10000

                        # 获取随机guid
                        case_date = crt_time.strftime("%Y%m")
                        guid = common_tools.get_rand_guid(t_url, u_price, case_date)  # id 用单价和链接+当前月份
                        str_crt_time = crt_time.strftime("%Y-%m-%d %H:%M:%S")

                        # 小区名称 和 地址
                        plot_name = item.xpath(".//dd/p[@class='add_shop']/a/@title")[0]  # 楼盘名称
                        addr = item.xpath(".//dd/p[@class='add_shop']/span/text()")[0].split('-')
                        loop = addr[0]  # 片区
                        address = addr[1]  # 地址

                        # 房屋信息
                        house_type = ""  # 户型
                        house_area = ""  # 面积
                        floor_no = ""  # 楼层
                        orientation = ""  # 朝向
                        build_date = ""  # 建筑年代
                        total_floor_num = ""  # 总楼层
                        desc = item.xpath(".//dd/p[1]")[0].xpath("string(.)").replace('\r\n', '').replace(' ', '')
                        flags = desc.split('|')
                        for fflag in flags:
                            if '室' in fflag:
                                house_type = fflag  # 户型
                                # dic.update({'户型': flag})
                            if '㎡' in fflag or '平米' in fflag:
                                house_area = re.findall('(\d+(\.\d+)?)', fflag)[0][0]  # 面积
                            if '层' in fflag:
                                floor_no = fflag  # 楼层
                            if '向' in fflag:
                                orientation = fflag.replace('向', '')  # 朝向
                            if '年建' in fflag:
                                build_date = re.match('\d+', fflag).group()  # 建筑年代

                        if len(floor_no) > 0:
                            p = floor_no
                            t1 = '层' in p
                            t2 = '共' in p
                            if t1 and t2:
                                s_str = re.match('(.*?)（共(.*?)）', p)
                                floor_no = s_str.group(1)  # 楼层
                                total_floor_num = s_str.group(2)  # 总楼层
                            else:
                                floor_no = p
                        dic_page = {"_id": guid,
                                    "city": sub_info["city"],
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
                                    "address": address,
                                    "project_name": plot_name,
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
                    except Exception as e:
                        logger.error("解析数据异常{}, {}".format(e, traceback.format_exc()))

                    else:
                        data_list.append(dic_page)  # 将数据字典添加到列表

            # page_data = content.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]
            # page_url = content.xpath("//div[@class='page-box house-lst-page-box']/@page-url")[0]  # 一页链接
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
               'User-Agent': 'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)'}
    resp = requests.get(
        url,
        headers=headers)
    content = etree.HTML(resp.content.decode("utf-8"))
    html_str = {"str": resp.content.decode("utf-8")}
    logger = logging.getLogger("")
