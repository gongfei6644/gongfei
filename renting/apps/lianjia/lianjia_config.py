import traceback
from urllib.parse import urljoin

from lxml import etree
from pymongo import UpdateOne, MongoClient, InsertOne
from requests import HTTPError

from setting import config
from utils.common_downloader_list import crawling
from utils.common_logger import get_logger
from utils.common_tools import check_cityname, get_rand_guid, get_full_url, check_area

dowloader = crawling()


def get_city(url):
    city_content = downloader.get_by_abucloud(start_url)
    if city_content != "retry":
        city_html = etree.HTML(city_content)
        city_nodes = city_html.xpath('//div[@class="city_province"]/ul/li')
        for node in city_nodes:
            city = node.xpath('string(./a/text())').strip()
            if city not in {"台湾", "香港", "澳门", ""}:
                city = check_cityname(city)
                city_href = node.xpath('string(./a/@href)').strip()
                city_url = get_full_url(url, city_href) + "zufang/"
                get_area(city_url, city)
    else:
        raise HTTPError("获取index失败")


city_fail = []
area_fail = []


def get_area(city_url, city):
    try:
        length = 8 if city_url.startswith("https") else 7
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            # 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            "Host": city_url[length:].split("/")[0]}
        area_content = downloader.get_by_abucloud(city_url, headers)
        if area_content != "retry":
            area_html = etree.HTML(area_content)
            area_nodes = area_html.xpath('//ul[@data-target="area"]/li[@data-type="district"]')
            for area_node in area_nodes:
                area = area_node.xpath('string(./a/text())').strip()
                if check_area(area):
                    area_href = area_node.xpath('string(./a/@href)').strip()
                    area_url = get_full_url(city_url, area_href)
                    get_sub(area_url, area, city)
        else:
            city_fail.append((city_url, city))
    except:
        city_fail.append((city_url, city))


def get_sub(area_url, area, city):
    condition = []
    try:
        sub_content = downloader.get_by_abucloud(area_url)
        if sub_content != "retry":
            sub_html = etree.HTML(sub_content)
            sub_nodes = sub_html.xpath('//ul[@data-target="area"][2]/li[@data-type="bizcircle"]')
            for sub_node in sub_nodes:
                sub = sub_node.xpath('string(./a/text())').strip()
                if check_area(sub):
                    item = {}

                    sub_href = sub_node.xpath('string(./a/@href)').strip()
                    sub_url = get_full_url(area_url, sub_href)
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


if __name__ == '__main__':
    source = "链家租房"
    start_url = "https://www.lianjia.com/city/"
    config_logger = get_logger("config", source, config.CONFIG_LOG_DIR)
    downloader = crawling(source, config_logger)
    client = MongoClient(config.MONGO_URI)
    db = client["DataCollecting"]
    tb = db["config"]
    get_city(start_url)
    print(city_fail)
    print(area_fail)
