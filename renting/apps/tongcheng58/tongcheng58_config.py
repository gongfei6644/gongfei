import random
import re
import time
import traceback

import requests
from lxml import etree
from pymongo import UpdateOne, MongoClient, InsertOne
from requests import HTTPError
from requests.exceptions import ProxyError
from collections import ChainMap
from setting import config
from utils.common_logger import get_logger

from utils.common_tools import check_cityname, get_rand_guid, get_full_url, check_area
from utils.constants import RETRY_TIMES_MAP
from utils.common_downloader_config import get_by_abucloud


def get_city(url):
    headers = {
        "cache-control": "no-cache",
    }
    city_content = get_by_abucloud(source,self_logger,url, headers)
    if city_content != "retry":
        r = re.findall(r'cityList = (.*?)<', city_content, re.S)
        data = eval(r[0].strip())
        all_data = ChainMap(*list(data.values()))
        for city, info in all_data.items():
            if city not in {"台湾", "香港", "澳门", ""}:
                city = check_cityname(city)
                py = info.split("|")[0]
                city_url = "https://{}.58.com/chuzu/?pagetype=area".format(py)
                get_area(city_url, city)
    else:
        raise HTTPError("获取index失败")


city_fail = []
area_fail = []


def get_area(city_url, city):
    try:
        area_content = get_by_abucloud(source,self_logger,city_url)
        if area_content != "retry":
            area_html = etree.HTML(area_content)
            area_nodes = area_html.xpath('//dl[@class="secitem secitem_fist"]//a')
            for area_node in area_nodes:
                area = area_node.xpath('string(./text())').strip()
                if check_area(area):
                    area_href = area_node.xpath('string(./@href)')
                    area_url = get_full_url(city_url, area_href)
                    get_sub(area_url, area, city)
        else:
            city_fail.append((city_url, city))
    except:
        print(traceback.print_exc())
        city_fail.append((city_url, city))


def get_sub(area_url, area, city):
    condition = []
    try:
        sub_content = get_by_abucloud(source,self_logger,area_url)
        if sub_content != "retry":
            sub_html = etree.HTML(sub_content)
            sub_nodes = sub_html.xpath('//dl[@class="secitem secitem_fist"]//a')
            for sub_node in sub_nodes:
                sub = sub_node.xpath('string(./text())').strip()
                if check_area(sub):
                    item = {}

                    sub_href = sub_node.xpath('string(./@href)').strip()
                    sub_url = get_full_url(area_url, sub_href).replace("?pagetype=area", "")
                    uid = get_rand_guid(source, city, sub_url)
                    item["_id"] = uid
                    item["source"] = source
                    item["city"] = city
                    item["area"] = area
                    item["sub_area"] = sub
                    item["sub_area_url"] = sub_url
                    op = InsertOne(item)
                    condition.append(op)
        else:
            area_fail.append((area_url, area, city))
    except:
        print(traceback.print_exc())
        area_fail.append((area_url, area, city))
    else:
        try:
            tb.bulk_write(condition, ordered=False)
        except Exception as e:
            print(e)


# def get_by_abucloud(url, headers=None, encoding="utf-8"):
#     '''
#     :param url: 爬取的url ，为空则默认类中的url
#     :param headers: 请求头，为空则默认类中的 headers
#     :param encoding: 页面编码，默认utf-8
#     :return: content 有3种状态: 正常网页数据的str / "404" / "retry"
#     '''
#     self_logger.info("进入下载:{}".format(url))
#     self_headers = {'User-Agent': random.choice(config.AGENT_LIST)}
#     self_proxy = config.ABY_URI
#     if headers:
#         self_headers.update(headers)
#     content = ""
#     for i in range(300):
#         try:
#             response = requests.get(url, headers=self_headers, proxies={
#                 "http": self_proxy, "https": self_proxy}, timeout=30, verify=False)
#             self_logger.info("第{}次重试,code:{}".format(i, response.status_code))
#             self_logger.info("\n访问链接 {}\n返回链接 {}".format(url, response.url))
#             if response.status_code == 200 and "verify" not in response.url:
#                 content = response.content.decode(encoding, "ignore")
#                 break
#             elif response.status_code == 404 or "/404." in response.url:
#                 content = "404"
#                 break
#             else:
#                 content = "retry"
#                 # self_logger.info("{}进入retry, code:{}".format(url, response.status_code))
#         except ProxyError as e:
#             # 未获取到隧道资源,返回重试标识
#             content = "retry"
#             self_logger.info("第{}次重试,代理异常: {}".format(i, e))
#         except Exception as ex:
#             content = "retry"
#             self_logger.error("第{}次重试,出现异常,错误信息：{}".format(i, ex))
#     else:
#         self_logger.info("连续{}次请求失败{}".format(RETRY_TIMES_MAP[source], url))
#     time.sleep(0.5)
#     return content


if __name__ == '__main__':
    source = "58同城租房"
    start_url = "https://www.58.com/changecity.html?catepath=chuzu"
    self_logger = get_logger("config", source, config.CONFIG_LOG_DIR)
    client = MongoClient(config.MONGO_URI)
    db = client["DataCollecting"]
    tb = db["config"]
    get_city(start_url)
    print(city_fail)
    print(area_fail)
