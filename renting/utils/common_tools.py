# coding=utf-8
import hashlib
import os
import random
import re
import time
from functools import wraps
from urllib.parse import urljoin
from hashlib import md5

import execjs
from w3lib.url import canonicalize_url
from setting import config
from utils.common_mysql import get_pagesize_config
from utils.common_redis import conn
from utils.constants import SPLIT_TABLE_NUM

website_pagesize = {}
log_path = config.LIST_LOG_DIR


def get_rand_guid(url, unit_price, ym):
    # ym = datetime.datetime.now().strftime("%Y%m")
    url = canonicalize_url(url)
    full = "{}{}{}".format(url, unit_price, ym).encode("utf-8")
    md5 = hashlib.md5()
    md5.update(full)
    guid = md5.hexdigest()
    return guid


def check_cityname(city_name):
    names = ['地区', '自治', '群岛', '县', '海域']
    for name in names:
        if name in city_name or city_name in {"阿拉善盟", "锡林郭勒盟", "兴安盟", "神农架林区"}:
            result = city_name
            break
        else:
            result = city_name if city_name.endswith("市") else city_name + "市"

    return result


def make_urls(sub_info):
    '''
    通过片区的初始url生成片区所有页码的urls
    '''
    page_urls = []
    total_pages = get_page_size(sub_info["source"], sub_info["city"])
    if sub_info["source"] == "城市房产租房":
        part_cityhouse = list(sub_info["sub_area_url"].partition("/lease/"))
        part_cityhouse[-1] = part_cityhouse[-1].rstrip("/") + "-pn{}/"
        # part_cityhouse[-1] = part_cityhouse[-1].rstrip("/") + "-pg{}/"
        base_cityhouse = "".join(part_cityhouse)
        page_urls = [base_cityhouse.format(i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]
        # print(page_urls)
    elif sub_info["source"] == "链家租房":
        page_urls = ["{}pg{}rco11/".format(sub_info["sub_area_url"], i + 1) if i else sub_info["sub_area_url"] + "rco11/" for i in range(total_pages)]
    elif sub_info["source"] == "中国房产超市租房":
        page_urls = ["{}_p{}.html".format(
            sub_info["sub_area_url"].replace(".html", ""), i + 1) for i in range(total_pages)]
    elif sub_info["source"] == "房天下租房":
        sub_url = sub_info["sub_area_url"].replace("http:", "https:")
        # page_urls = ["{}h31-i3{}/".format(
        #     sub_url, i + 1) if i else sub_url + "h31/" for i in range(total_pages)]
        page_urls = ["{}{}/".format(
            sub_url, 'i'+str(30+i+1)) if i else sub_url  for i in range(total_pages)]
        # page_urls = [url.replace("esf1", "esf") + "?_rfss=1" for url in page_urls]

    elif sub_info["source"] == "安居客租房":
        page_urls = ["{}p{}-px3/".format(
            sub_info["sub_area_url"], i + 1) if i else sub_info["sub_area_url"] + "px3/" for i in range(total_pages)]
    elif sub_info["source"] == "中原地产租房":
        page_urls = ["{}/u7g{}/".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] + "u7/" for i in range(total_pages)]
    elif sub_info["source"] == "诸葛找房租房":
        page_urls = ["{}/page/{}/".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]
    elif sub_info["source"] == "赶集网租房":
        page_urls = ["{}/pn{}/".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]
    elif sub_info["source"] == "58同城租房":
        page_urls = ["{}/pn{}/".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]
    elif sub_info["source"] == "Q房网租房":
        page_urls = ["{}/f{}".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]

    return page_urls


def get_page_size(source, city_name):
    '''
     按网站来源，城市，获取网站最大采集页数
    :param source:数据源网站
    :param city_name:城市名
    :return: page_size
    '''
    global website_pagesize
    if website_pagesize == {}:
        website_pagesize = get_pagesize_config()
    first_tier_cities_list = {"北京市", "上海市", "广州市", "深圳市"}
    city_key = "generic_city"
    # 判断是否为一线城市
    if city_name in first_tier_cities_list:
        city_key = "first_tier_cities"
    page_size = website_pagesize.get(source, {}).get(city_key, 30)
    return page_size


class ClsSingleton():
    """单例基础类"""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_the_instance'):
            cls._the_instance = object.__new__(cls)
        return cls._the_instance


def format_num(t):
    """数字元组转成数字"""
    r = 0
    if isinstance(t, tuple):
        try:
            for i, v in enumerate(t):
                r += int(v) * 10 ** ((len(t) - 1 - i) * 3)
                r = str(r)
        except:
            pass
    elif isinstance(t, str):
        r = t.replace(",", "")
    else:
        r = t
    return r


def timeit(func):
    """定义装饰器的函数"""
    @wraps(func)
    def inner(*args, **kwargs):
        """内层函数"""
        st = time.time()
        result = func(*args, **kwargs)
        et = time.time()
        print("execute the function cost:{}".format(et - st))
        return result
    return inner


@timeit
def function(a):
    """被装饰函数"""
    print("here is func, param is {}".format(a))


def get_full_url(url, href):
    if href.startswith("http"):
        full_url = href
    elif href.startswith("//"):
        full_url = "https:" + href if url.startswith("https") else "http:" + href
    else:
        full_url = urljoin(url, href)
    return full_url


def check_area(area):
    if not any([not area, "周边" in area, "旅游" in area, "风景" in area, "名胜" in area, "其他" in area,
                "其它" in area, "周边" in area, "不限" == area, "全部" == area]):
        return True
    return False


def format_num(param):
    """格式化数字"""
    param = str(param).replace(",", "")
    try:
        param_str = re.sub(r'\s+', '', param)
        num_str = re.findall(r'\d+\.?\d*', param_str)
        num = float(num_str[0])
        if "万" in num_str:
            num *= 10000
    except:
        num = None
    return num


def get_proxy_ip(p_source):
    num = 0
    while True:
        try:
            ip_list = conn.keys()
            ip = random.choice(ip_list)
            valid_time = conn.ttl(ip)
            # print('ip剩余有效时间：%ds,网站：%s'%(valid_time,conn.get(ip)))
            print('ip剩余有效时间：%ds' % valid_time)
            if p_source not in conn.get(ip) and valid_time >= 65:
                    break
            else:
                num += 1
                time.sleep(0.00001)
            if num > 20:
                ip = random.choice(ip_list)
                if p_source not in conn.get(ip) and valid_time >= 30:
                    num = 0
                    break
            if num > 30:
                if valid_time >= 65:
                    break
            if num > 40:
                time.sleep(1)
        except:
            continue
    return ip


# 获取表名
def table_name(base_table, idx):
    table = base_table + '_{}'.format(str(idx))
    if idx < 10:
        table = base_table + '_0{}'.format(str(idx))
    return table


# 获取表名
def table_name_by_city(base_table, city):
    return table_name(base_table, table_idx(city))


# 获取城市对应的表索引
def table_idx(city):
    hash_code = int(md5(city.encode('UTF-8')).hexdigest(), 16)
    idx = hash_code % SPLIT_TABLE_NUM
    return idx


if __name__ == '__main__':
    function("000")
    format_num(12)
