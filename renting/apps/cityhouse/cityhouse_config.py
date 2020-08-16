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
from utils.common_downloader_config import get_by_abucloud
from utils.constants import RETRY_TIMES_MAP, CITIES


def get_city(url):
    condition = []
    headers = {
        "cache-control": "no-cache",
    }
    city_content = get_by_abucloud(source,self_logger,url, headers)
    if city_content != "retry":
        city_html = etree.HTML(city_content)
        city_nodes = city_html.xpath('//a[@class="first"]')
        for node in city_nodes:
            city = node.xpath('string(.)').strip()
            # if city not in CITIES:  # 获取指定城市
            if city not in {"台湾", "香港", "澳门", ""}:
                city = check_cityname(city)
                city_href = node.xpath('string(./@href)').strip()
                city_url = city_href + "/lease/"
                # print(city, city_url)
                if city in {"北京市", "上海市", "广州市", "深圳市"}:
                    get_area(city_url, city)
                else:
                    item = {
                        "_id": get_rand_guid(source, city, city_url),
                        "source": source,
                        "city": city,
                        "sub_area_url": city_url
                    }
                    op = InsertOne(item)
                    condition.append(op)
        try:
            tb.bulk_write(condition, ordered=False)
        except Exception as e:
            print(e)
    else:
        raise HTTPError("获取index失败")


city_fail = []
area_fail = []


def get_area(city_url, city):
    condition = []
    try:
        area_content = get_by_abucloud(source,self_logger,city_url)
        if area_content != "retry":
            area_html = etree.HTML(area_content)
            area_nodes = area_html.xpath(
                '//div[@class="housearea_listbox"]/div[@class="housearea_list"][1]//a[not(contains(text(), "全市")) and not(contains(text(), "全区"))]')
            for area_node in area_nodes:
                item = {}
                area = area_node.xpath('string(./text())').strip()
                if check_area(area):
                    area_href = area_node.xpath('string(./@href)')
                    area_url = get_full_url(city_url, area_href)

                    sub_url = area_url
                    item["_id"] = get_rand_guid(source, city, sub_url)
                    item["source"] = source
                    item["city"] = city
                    item["area"] = area
                    item["sub_area"] = ""
                    item["sub_area_url"] = sub_url
                    op = InsertOne(item)
                    condition.append(op)


        else:
            city_fail.append((city_url, city))
    except:
        print(traceback.print_exc())
        city_fail.append((city_url, city))
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
#     self_proxy = config.ABY_URI_MAP.get(source, config.ABY_URI_LIST)
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
    source = "城市房产租房"
    start_url = "http://www.cityhouse.cn/city.html"
    self_logger = get_logger("config", source, config.CONFIG_LOG_DIR)
    client = MongoClient(config.MONGO_URI)
    db = client["DataCollecting"]
    tb = db["config"]
    get_city(start_url)
    print(city_fail)
    print(area_fail)
