import traceback
from urllib.parse import urljoin

from lxml import etree
from pymongo import UpdateOne, MongoClient, InsertOne
from requests import HTTPError

from setting import config
from utils.common_downloader_list import crawling
from utils.common_logger_list import get_logger
from utils.common_tools import check_cityname, get_rand_guid

dowloader = crawling()
def get_city(url):
    city_content = downloader.get_by_abucloud(start_url)
    if city_content != "retry":
        city_html = etree.HTML(city_content)
        city_nodes = city_html.xpath('//div[@class="all-city"]//a')
        print("city_nodes:", len(city_nodes))
        for node in city_nodes:
            city = node.xpath('string(./text())').strip()
            if city not in {"台湾", "香港", "澳门", ""}:
                city = check_cityname(city)
                city_href = node.xpath('string(./@href)')
                city_url = city_href + "ershoufang/"
                get_area(city_url, city)
    else:
        raise HTTPError("获取index失败")
city_fail = []
area_fail = []
condition = []
def get_area(city_url, city):
    try:
        area_content = downloader.get_by_abucloud(city_url)
        if area_content != "retry":
            area_html = etree.HTML(area_content)
            area_nodes = area_html.xpath('//ul[@class="f-clear"]/li/a')
            print("area_nodes", len(area_nodes))
            for area_node in area_nodes:
                area = area_node.xpath('string(./text())').strip()
                if not any(["周边" in area, "旅游" in area, "风景" in area, "名胜" in area, "其他" in area,
                            "其它" in area, "不限" in area, "周边" in area, area == ""]):
                    area_href = area_node.xpath('string(./@href)')
                    area_url = "http:" + area_href if area_href.startswith("//") else urljoin(city_url, area_href)
                    get_sub(area_url, area, city)
        else:
            city_fail.append((city_url, city))
    except:
        print(traceback.print_exc())
        city_fail.append((city_url, city))




def get_sub(area_url, area, city):
    try:
        sub_content = downloader.get_by_abucloud(area_url)
        if sub_content != "retry":
            sub_html = etree.HTML(sub_content)
            sub_nodes = sub_html.xpath('//div[@class="fou-list f-clear"]//a')
            print("sub_nodes", len(sub_nodes))
            for sub_node in sub_nodes:
                sub = sub_node.xpath('string(./text())').strip()
                print("sub", sub)
                if not any(["周边" in sub, "旅游" in sub, "风景" in sub, "名胜" in sub, "其他" in sub,
                            "其它" in sub, "不限" in sub, "周边" in sub, sub == ""]):
                    item = {}

                    sub_href = sub_node.xpath('string(./@href)')
                    sub_url = "http:" + sub_href if sub_href.startswith("//") else urljoin(area_url, sub_href)
                    uid = get_rand_guid(city, sub, sub_url)
                    item["_id"] = uid
                    item["source"] = source
                    item["city"] = city
                    item["area"] = area
                    item["sub_area"] = sub
                    item["sub_area_url"] = sub_url
                    print("11111", item)
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
    source = "赶集网二手房"
    start_url = "http://www.ganji.com/index.htm"
    config_logger = get_logger("config", source, config.LIST_LOG_DIR)
    downloader = crawling(source, config_logger)
    client = MongoClient(config.MONGO_URI)
    db = client["DataCollecting"]
    tb = db["ganji_config_new"]
    get_city(start_url)
    print(city_fail)
    print(area_fail)
