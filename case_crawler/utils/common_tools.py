# coding=utf-8
import hashlib
import re
import time
from functools import wraps
from w3lib.url import canonicalize_url
from setting import config
from utils.common_mysql import get_pagesize_config
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
    if sub_info["source"] == "城市房产二手房":
        page_urls = ["{}/pg{}/".format(
            sub_info["sub_area_url"].strip("/"), i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]
    elif sub_info["source"] == "链家二手房":
        page_urls = ["{}/pg{}co32/".format(sub_info["sub_area_url"].replace(
            "/co32/", ""), i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]
    elif sub_info["source"] == "中国房产超市二手房":
        page_urls = ["{}_p{}.html".format(
            sub_info["sub_area_url"].replace(".html", ""), i + 1) for i in range(total_pages)]
    elif sub_info["source"] == "房天下二手房":
        sub_url = sub_info["sub_area_url"].replace("http:", "https:")
        page_urls = ["{}-i3{}/".format(
            sub_url.strip("/"), i + 1) if i else sub_url for i in range(total_pages)]
        if sub_info['city'] == "北京市":
            page_urls = [url.replace("esf1", "esf") + "?_rfss=1" for url in page_urls]

    elif sub_info["source"] == "安居客二手房":
        page_urls = ["{}/o5-p{}/".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] + "o5/" for i in range(total_pages)]
    elif sub_info["source"] == "中原地产二手房":
        page_urls = ["{}/u7g{}/".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] + "u7/" for i in range(total_pages)]
    elif sub_info["source"] == "诸葛找房二手房":
        page_urls = ["{}/page/{}/".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]
    elif sub_info["source"] == "赶集网二手房":
        page_urls = ["{}/pn{}/".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]
    elif sub_info["source"] == "58同城二手房":
        page_urls = ["{}/pn{}/".format(sub_info["sub_area_url"].strip(
            "/"), i + 1) if i else sub_info["sub_area_url"] for i in range(total_pages)]
    elif sub_info["source"] == "Q房网二手房":
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

def format_date(date_str):
    r = re.findall('更新于(.*日)')

if __name__ == '__main__':
    function("000")
