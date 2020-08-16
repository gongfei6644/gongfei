import copy
import time
import traceback
from urllib.parse import urljoin

import requests
from lxml import etree

from utils.common_downloader_list import crawling
from utils.common_mongo import MongoOption

headers = {
# ":authority":"sz.centanet.com",
# ":method":"GET",
# ":path":"/ershoufang/",
# ":scheme":"https",
# "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
# "accept-encoding":"gzip, deflate, br",
# "accept-language":"en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
# "cache-control":"no-cache",
# "cookie":"Y190cmFja2lk=c9a8aa2d857847aaad495db5bbf30c8e; gr_user_id=ac951470-9f9c-4314-b325-6c72c2fd72c1; grwng_uid=1a63e77d-b45d-4cfa-bc50-885d6eea891d; 400cookiesem=baidu&BSPAALC92639832; _pk_ref.2.ad93=%5B%22%22%2C%22%22%2C1555732702%2C%22https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.af0000aF4eAvq9HI845w_y3HmqiN2Z0PmBBD__xyucwUOtwxdNN3NWY4XOzkr5_oiFqf6fuEvtU8D4-wn_fRdY1LYFpUpswur5cgm2kXD6Et6knv9ApE0dLECMo4BZDzF1HI6ttyidnQpdFZvgMoMeMvcot_gGK14Vcq4w-asRUxMc70crCS8K1dWETNy7smOKFRmoxsjFSbO7GCvs.7R_NR2Ar5Od66W3x27nNKhFPKDZfq-L_sfIZ_134GohyUVyEN0h5gKLWHGmEukmrVyMZwmqxkOPexUSE3ISHG3eqMZcGyAp7WG3Sr1BC.U1Y10ZDq_tx2YQXO_EJvO_oyVet0TA-W5H00Ijv1ktofVJEgSUUSzVpLEqj71lc0pyYqnWcd0ATqmhNsT100Iybqmh7GuZR0TA-b5Hf0mv-b5Hb10AdY5HDsnHIxnH0krNtznjmzg1nvnjD0pvbqn0KzIjYvPWc0uy-b5HDYPHwxnWDsrjNxnW6LPW9xnW6LnWPxnW6dPH9xnW63n1NxnW6drjwxnW6vnjn0mhbqnW0Yg1DdPfKVm1Y3njbdnj03P1KxnH0snNtkrHbzPH63nH6dg100TgKGujYs0Z7Wpyfqn0KzuLw9u1Ys0A7B5HKxn0K-ThTqn0KsTjYs0A4vTjYsQW0snj0snj0s0AdYTjYs0AwbUL0qn0KzpWYs0Aw-IWdsmsKhIjYs0ZKC5H00ULnqn0KBI1Ykn0K8IjYs0ZPl5fK9TdqGuAnqTZnVuLGCXZb0IZN15HDvnWmvrjRknHDzPjTLPHbYnHD0ThNkIjYkPHRdP1nzPW6Yn1Tk0ZPGujdWrHRYnvR4rH0snAD3rHR30AP1UHdjrDR4nW63wDfYf1uanjDd0A7W5HD0TA3qn0KkUgfqn0KkUgnqn0KlIjYs0AdWgvuzUvYqn7tsg1Kxn0Kbmy4dmhNxTAk9Uh-bT1Ysg1Kxn7ts0ZK9I7qhUA7M5H00uAPGu%22%5D; _pk_ses.2.ad93=*; Hm_lvt_5ba699e44b8a99227ac7a04f91a66196=1555386175,1555503530,1555732702; a3737a846d019278_gr_session_id=1d4f6366-8fea-47fc-a9b9-f00f46020e99; a3737a846d019278_gr_session_id_1d4f6366-8fea-47fc-a9b9-f00f46020e99=true; _pk_id.2.ad93=f85ee28f1a5527f6.1555386175.3.1555733513.1555732702.; Hm_lpvt_5ba699e44b8a99227ac7a04f91a66196=1555733513",
"pragma":"no-cache",
# "upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
}
downloader = crawling("中原地产二手房")
db = MongoOption()

def city_config(city, city_url):
    # "https://sz.centanet.com/ershoufang/"
    print(city_url)
    resp_city = requests.get(city_url, headers=headers)
    print(resp_city.status_code)
    html = etree.HTML(resp_city.text)
    if resp_city.status_code == 200:
        a_nodes = html.xpath('//p[@class="termcon"]/a')
        for a in a_nodes:
            area = a.xpath('string(./text())')
            area_href = a.xpath('string(./@href)')  # /ershoufang/nanshan/
            # area_url  = "https://sz.centanet.com/ershoufang/nanshan/"
            area_url = city_url.replace("/ershoufang/", area_href)
            print(area_url)
            resp_area = requests.get(area_url, headers=headers, timeout=15, verify=False)
            time.sleep(2)
            if resp_area.status_code == 200:
                subarea_nodes = html.xpath('//p[@class="subterm"]/a')
                for sub in subarea_nodes:
                    item = {}
                    sub_area = sub.xpath('string(./text())')
                    sub_area_href = sub.xpath('string(./@href)')
                    sub_area_url = city_url.replace("/ershoufang/", sub_area_href)

                    item["source"] = source
                    item["city"] = city
                    item["area"] = area
                    item["sub_area"] = sub_area
                    item["sub_area_url"] = sub_area_url


def zhongyuan_city(start_url):
    resp_start = requests.get(start_url, headers=headers)
    time.sleep(2)
    if resp_start.status_code == 200:
        start_html = etree.HTML(resp_start.text)
        city_nodes = start_html.xpath('//a[@class="f000"]')[2:3]
        print("共计{}个城市".format(len(city_nodes)))
        item_list = []
        for city_node in city_nodes:
            item = {}
            city = city_node.xpath('string(./text())')
            city_href = city_node.xpath('string(./@href)')
            city_url = city_href + "ershoufang/"
            print(city, city_url)
            # city_config(city, city_url)
            item["_id"] = city_url
            item["city"] = city
            item["city_url"] = city_url
            item["status"] = 0
            return item
            item_list.append(item)
        # try:
        #     db.m_insert(item_list, "zhongyuan_city_new")
        # except Exception as e:
        #     print(e)

def zhongyuan_area():
    city_infos = list(db.m_select({'city': "深圳"}, "zhongyuan_city_new"))
    print("共计{}个城市".format(len(city_infos)))
    for city_info in city_infos:
        try:
            resp_area = requests.get(city_info["city_url"], headers=headers)
        except:
            print("请求失败{}".format(city_info))
            time.sleep(5)
        try:
            if resp_area.status_code == 200:
                html_area = etree.HTML(resp_area.text)
                a_nodes = html_area.xpath('//ul[@class="tagbox_wrapper_m_ul tap_show"]/li/a | //p[@class="termcon"]/a')
                print("{}共计{}个行政区".format(city_info["city"], len(a_nodes)))
                item_list = []
                for a in a_nodes:
                    item_area = {}
                    area = a.xpath('string(./text())').strip()
                    if not any(["周边" in area, "旅游" in area, "风景" in area, "名胜" in area, "其他" in area,
                         "其它" in area, "不限" in area, "周边" in area]):
                        area_href = a.xpath('string(./@href)').strip()
                        area_url = city_info["city_url"].replace("/ershoufang/", area_href)
                        item_area["city"] = city_info["city"] if city_info["city"] .endswith("市") else city_info["city"] + "市"
                        item_area["area"] = area
                        item_area["_id"] = area_url
                        item_area["area_url"] = area_url
                        item_area["status"] = 0

                        item_list.append(item_area)
                try:
                    db.m_insert(item_list, "zhongyuan_area_new")
                except Exception as e:
                    print(e)
        except:
            print(traceback.print_exc())
        else:
            city_finish = copy.deepcopy(city_info)
            city_finish["status"] = 1
            db.s_update({"_id": city_info["_id"]}, city_finish, "zhongyuan_city_new")
            pass


def zhongyuan_sub():
    area_infos = list(db.m_select({'city': "深圳"}, "zhongyuan_area_new"))
    print("共计{}个行政区".format(len(area_infos)))
    item_list = []
    for index, area_info in enumerate(area_infos):
        try:
            resp_area = requests.get(area_info["area_url"], headers=headers)

        except:
            print(index, "------------------")

            print("请求失败{}".format(traceback.format_exc()))
            time.sleep(5)
        else:
            if resp_area.status_code == 200:
                html_area = etree.HTML(resp_area.text)
                s_nodes = html_area.xpath('//p[@class="subterm"]//a | //ul[@class="tagbox_wrapper_cd_ul tap_show"]/li/a')
                print("{}{}共计{}个片区".format(area_info["city"], area_info["area"], len(s_nodes)))

                for s in s_nodes:
                    item_sub = {}
                    sub_area = s.xpath('string(./text())').strip()
                    sub_href = s.xpath('string(./@href)').strip()  # /ershoufang/nanshan/
                    sub_url = urljoin(area_info["area_url"], sub_href)
                    item_sub["source"] = source
                    item_sub["city"] = area_info["city"] if area_info["city"].endswith("市") else area_info["city"] + "市"
                    item_sub["area"] = area_info["area"]
                    item_sub["_id"] = sub_url
                    item_sub["sub_area"] = sub_area

                    item_sub["sub_area_url"] = sub_url
                    item_list.append(item_sub)

    print(len(item_list))

    try:
        db.m_insert(item_list, "zhongyuan_sub_new")
    except Exception as e:
        print(e)
        print(traceback.print_exc())








if __name__ == '__main__':
    source = "中原地产二手房"
    start_url = "https://sz.centanet.com"

    # zhongyuan_city(start_url)
    # zhongyuan_area()
    zhongyuan_sub()
