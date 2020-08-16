# coding=utf-8
import os
import re
import json
import datetime
import time
import traceback
from math import ceil
from urllib.parse import urljoin

import execjs
from lxml import etree

from utils import common_tools
from utils.common_downloader_list import crawling
from utils.common_tools import get_rand_guid, format_num, get_page_size, get_full_url

page_count = 20  # post请求每页案例数


def list_chengshifangchan(logger, content, sub_info):
    """
    解析城市房产租房
    :param logger: 日志管理器
    :param content: HTML对象
    :param sub_info: 片区信息
    :return: {"data": data_list, "flag": flag}, flag有2种状态: "finish" / "normal"
    """
    # print(content)
    logger.info("进入解析函数,{}".format(sub_info["page_url"]))
    crawling_model = crawling(sub_info["source"], logger)
    flag = "normal"
    data_list = []
    if content == "404":
        flag = "finish"
    elif content != "retry":
        html = etree.HTML(content)
        try:
            projects = html.xpath('//div[@class="houselist_singlearea"]')  # 小区列表
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for project in projects:
                hacode = project.xpath("string(./@hacode)")
                page_index = 0
                while True:
                    try:
                        json_data = get_page_by_post(sub_info, hacode, crawling_model, page_index)
                    except Exception as e:
                        logger.error("获取数据异常: {} \n{}".format(e, traceback.format_exc()))
                    else:
                        if json_data:
                            data_post = parse_data(sub_info, json_data)
                            data_list.extend(data_post)
                            if not data_list or len(data_post) < page_count:
                                logger.info("已解析数据:{}条, 当前小区{}条".format(len(data_list), len(data_post)))
                                break
                    finally:
                        page_index += 1

                        # 解析数据

            try:
                next_href = html.xpath("string(//a[@class='pgdn']/@href)")
                if not next_href or not projects:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))

    dic_data = {"data": data_list, "flag": flag}
    print(flag,dic_data)
    return dic_data


def get_page_by_post(sub_info, hacode, crawling_model, page_index=0):
    """
    生成请求数据, 调用post请求
    :param sub_info:片区信息
    :param hacode:小区代码
    :param page_index: p_page post数据的页码
    :param logger:日志管理器
    :return:dict_data 仔细点类型的数据
    """
    p_page = (re.findall(r'pg(\d*)', sub_info['page_url']) or ["1"])[0]  # p_page: list页的页码, 从1开始
    start_num = page_count * page_index + 1
    param_headers = {
                    "Referer": sub_info['page_url'],
                    'Accept': 'Accept-Encoding:gzip, deflateAccept-Language:zh-CN,zh;q=0.8',
                    "Cookie":'househistory=http%253A%252F%252Fqth.cityhouse.cn%252Flease%252F0000820816505.html@%u5317%u5CB8%u65B0%u57CE**90%u33A1*2%2C000; cityre=1efb15780e92fc6b64785aec0d4bd1da; Hm_lvt_435bf6d47bee0643980454513deeb34f=1566800214,1569313076,1569317327,1569319650; Hm_lpvt_435bf6d47bee0643980454513deeb34f=1569319650',
                    "Host": "wanning.cityhouse.cn",
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                     }
    data_param = {
        "hacode": hacode,
        "startnum": str(start_num),  # 请求案例的起始index
        "pagesize": page_count,  # 每次请求案例数
        "p[proptype]": "11",
        "p[pagesize]": "10",
        "p[flag]": "2",
        'p[page]': p_page,
    }
    url_prefix = sub_info["sub_area_url"].split("/lease")[0]
    url_param = "{}/forsale/listnewajax.html?hacode={}&pagesize={}&startnum={}".format(
        url_prefix, hacode, page_count, start_num)
    json_data = crawling_model.post(url_param, param_headers, data_param)
    json_data = parse_json_data(json_data)

    return json_data


def parse_data(sub_info, json_data):
    data_list = []

    if json_data:
        py_data = json.loads(json_data)
        data_items = py_data.get("items")
        # print(py_data)
        for item in data_items:

            now_time = datetime.datetime.now()  # 当前消息时间
            try:
                title = item.get("headline", "")
                total_price = format_num(item.get("totalPrice"))  # 总价
                total_price_unit = item.get("totalPriceUnit", "")
                total_price = total_price * 10000 if "万" in total_price_unit else total_price
                dealcode = item["dealCode"]
                # "http://hf.cityhouse.cn/lease/0473834398352.html"
                url_prefix = sub_info["sub_area_url"].split("/lease")[0]
                detail_url = "{}/lease/{}.html".format(url_prefix, dealcode)  # 详情链接

            except:
                pass
            else:
                case_date = now_time.strftime("%Y%m")
                guid = get_rand_guid(detail_url, total_price, case_date)
                try:
                    floor_no = item.get("floor", "")  # 楼层 3/11
                    floor_no = floor_no.split("/")[0]
                    total_floor_num = re.findall("\d+", item.get("floor2", ""))
                    if total_floor_num:
                        total_floor_num = total_floor_num[0]
                    else:
                        total_floor_num = ''
                except:
                    floor_no, total_floor_num = "", ""
                # 押付方式
                try:
                    house_type = item.get("huxing", "")  # 户型:2室2厅
                    r = title.findall(r'付\d+押\d+', title.split(house_type)[0])
                    rental_method = r[0] if r else ""
                except:
                    rental_method = ""
                try:
                    unitprice = round(float(item.get("unitPrice")), 2)
                except:
                    unitprice = ""


                area = item.get("distName")
                # publish_date = item.get("publishTime", "")[:10]  # 发布时间
                publish_date = format_date(item.get("flushTime", ""))  # 发布时间
                cur_date = datetime.datetime.now()

                if not any(["周边" in area, "旅游" in area, "风景" in area, "名胜" in area,
                            "其他" in area, "其它" in area, "不限" in area, "周边" in area,
                            (cur_date - datetime.datetime.strptime(publish_date, "%Y-%m-%d")).days > 62]):
                    dic_data = {
                        "_id": guid,
                        "list_page_url": sub_info["page_url"],
                        "city": sub_info["city"],
                        "title": title,
                        "source_link": detail_url,
                        "data_source": sub_info["source"],
                        "crt_time": now_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "build_area": str(item.get("bldgArea")),  # 面积 120㎡
                        "unitprice": unitprice,
                        "total_price": total_price,
                        "address": item.get("address", ""),  # 楼盘地址
                        "project_name": item.get("haName", ""),  # 楼盘名称
                        "house_type": item.get("huxing", ""),  # 户型
                        "floor_no": floor_no,
                        "total_floor_num": total_floor_num,
                        "orientation": item.get("face", ""),  # 朝向
                        "area": area,
                        "sub_area": "",
                        "case_happen_date": publish_date,
                        "gps": item.get("gps", ""),  # gps信息  '39.47491160593571,116.30321709971135'
                        "usage": item.get("propType", ""),  # 住宅
                        "rental_method": rental_method  # 押付类型
                    }

                    # print(dic_data)
                    data_list.append(dic_data)
        print(data_list)
        return data_list


def parse_json_data(json_data):
    try:
        returnCitySN = json_data[1]
        json_data = json_data[0]
        jsstr = returnCitySN
    except:
        return
    try:
        with open(os.path.join(os.path.abspath('.'),'apps/cityhouse/tools.js'),'r',encoding='gbk',errors="ignore") as f:
            jsstr += f.read()
        print(os.path.join(os.path.abspath('.'), 'apps/cityhouse/tools.js'))
    except:
        with open('/usr/projects/fxt_renting/apps/cityhouse/tools.js','r',encoding='gbk',errors="ignore") as f:
            jsstr += f.read()
    ctx = execjs.compile(jsstr)  # .compile
    return ctx.call('deBase64', json_data).encode('utf8').decode('unicode_escape').replace('\\','')



def format_date(p_date):
    if '小时前'in p_date:
        p_date = re.findall(r'(\d+)小时前',p_date)
        if p_date:
            p_date = (datetime.datetime.now()-datetime.timedelta(hours=int(p_date[0]))).strftime('%Y-%m-%d')
        else:
            p_date = ''
    elif '天前' in p_date:
        p_date = re.findall(r'(\d+)天前', p_date)
        if p_date:
            p_date = (datetime.datetime.now() - datetime.timedelta(days=int(p_date[0]))).strftime('%Y-%m-%d')
        else:
            p_date = ''
    else:
        p_date = p_date

    return p_date

