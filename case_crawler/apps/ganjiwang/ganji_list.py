# coding=utf-8
import logging
from urllib.parse import urljoin

from lxml import etree
import re
import datetime

import traceback

import requests

from utils.common_tools import get_rand_guid


def list_ganji(logger, content, sub_info):
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
            items = content.xpath(
                "//div[@class='f-list-item ershoufang-list']/dl[@class='f-list-item-wrap min-line-height f-clear']")
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, sub_info["page_url"]))
        else:
            for item in items:

                crt_time = datetime.datetime.now()  # 当前消息时间
                str_crt_time = crt_time.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    title = item.xpath("./dd[@class='dd-item title']/a/text()")[0]  # 标题
                    detail_url = item.xpath("./dd[@class='dd-item title']/a/@href")[0]  # 详情链接
                    t_url = detail_url if detail_url.startswith("http") else "http:" + detail_url
                    str_u_price = item.xpath("./dd[@class='dd-item info']/div[@class='time']/text()")[0]  # 单价
                    u_price = re.findall(r'\d+\.?\d*', str_u_price)[0]
                    if "万" in str_u_price:
                        u_price = float(u_price) * 10000
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

                    # 总价
                    try:
                        str_t_price = item.xpath(
                            "./dd[@class='dd-item info']/div[@class='price']/span[@class='num']/text()")[0]  # 总价
                    except Exception as error:
                        msg = "总价信息获取失败{}错误信息：{},{}".format(sub_info, error, traceback.format_exc())
                        logger.error(msg)
                        t_price = ""
                    else:
                        t_price = re.findall('\d+', str_t_price)[0]  # 总价


                    # 获取随机guid
                    case_date = crt_time.strftime("%Y%m")
                    guid = get_rand_guid(t_url, u_price, case_date)  # id 用单价和链接+当前月份
                    # 小区名称 和 地址
                    plot_name = ""  # 楼盘名称
                    address = ""  # 楼盘地址
                    try:
                        plot_name = item.xpath("./dd[@class='dd-item address']//span[@class='address-eara']/text()")[
                            0]  # 楼盘名称
                    except Exception as error:
                        pass
                    else:
                        if len(plot_name) > 0:
                            plot_name = plot_name.strip()

                    if len(plot_name) == 0:
                        msg = "没有找到楼盘名称,{}".format(sub_info["page_url"])
                        logger.info(msg)

                    try:
                        baseinfo_list = item.xpath("./dd[@class='dd-item size']/span")
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

                        if len(house_area) == 0:
                            msg = "关键字段缺失，{}".format(sub_info["page_url"])
                            logger.info(msg)

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
                    except Exception as error:
                        msg = "住宅信息获取失败，页面：{},错误信息：{}".format(sub_info["page_url"], error)


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
                                "build_date": build_date, "area": sub_info["area"],
                                "sub_area": sub_info["sub_area"],
                                "case_type_code": 3001001,
                                "list_page_url": sub_info["page_url"],
                                }

                    data_list.append(dic_page)  # 将数据字典添加到列表
            try:
                next_href = content.xpath("string(//a[@class='next']/@href)")
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
    sub_info = {}
    list_ganji(logger, html_str, sub_info)
