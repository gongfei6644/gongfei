# coding=utf-8

import re
import json
import datetime
import traceback
from math import ceil
from urllib.parse import urljoin
from utils import common_tools
from utils.common_downloader_list import crawling
from utils.common_tools import get_rand_guid, format_num, get_page_size


def list_chengshifangchan(logger, content, sub_info):
    """
    解析诸葛找房二手房
    :param logger: 日志管理器
    :param content: HTML对象
    :param sub_info: 片区信息
    :return: {"data": data_list, "flag": flag}, flag有2种状态: "finish" / "normal"
    """
    page_count = 50  # post请求每页案例数
    crawling_model = crawling(sub_info["source"], logger)
    page_index = 0
    retry_times = 3
    data_list = []
    flag = "normal"

    if content == "404":
        flag = "finish"
    elif content == "retry":
        flag = "normal"
    else:
        try:
            items = content.xpath("//div[@class='houselist_boxl fr']/div[@class='houselist_singlearea']")
        except Exception as e:
            logger.error("解析案例节点异常:{}, {}".format(e, traceback.format_exc()))
        else:
            for item in items:  # 每个item为一个小区
                hacode = item.xpath("string(./@hacode)")  # 楼盘code

                # 获取totalsize的循环
                for i in range(retry_times):
                    try:
                        dict_data = get_page_by_post(sub_info, hacode, crawling_model)
                        total_size = int(format_num(dict_data['totalSize']))
                        if total_size:
                            break
                        else:
                            raise ValueError("totalSize为空")
                    except Exception as e:
                        logger.error("获取到的数据不正常: {}.....".format(e))
                else:
                    total_size = 0
                    logger.error("解析post案例异常没有totalSize字段{}".format(sub_info["page_url"]))
                page_size_artifical = get_page_size(sub_info["source"], sub_info["city"])
                page_size_inherent = ceil(total_size / page_count) + 1
                page_size = min(page_size_artifical, page_size_inherent)
                for i in range(page_size):
                    dict_data = get_page_by_post(sub_info, hacode, crawling_model, i)
                    data_items = dict_data.get('items')
                    if not data_items:
                        break
                    else:
                        for item in data_items:
                            crt_time = datetime.datetime.now()  # 当前消息时间
                            str_crt_time = crt_time.strftime("%Y-%m-%d %H:%M:%S")
                            try:
                                title = item["headline"]
                                u_price = str(item["unitPrice"])
                                dealcode = item["dealCode"]  # 房屋编码，详情时会用到
                                t_url = "{}{}.html".format(sub_info["sub_area_url"], dealcode)  # 详情链接
                            except:
                                logger.error("缺少必要字段: 无效案例{}".format(sub_info))
                            else:
                                case_date = crt_time.strftime("%Y%m")
                                guid = get_rand_guid(t_url, u_price, case_date)
                                house_type = item.get("huxing", "")  # 户型
                                house_area = str(item.get("bldgArea"))  # 面积 120㎡
                                floor_no = item.get("floor", "")  # 楼层 3/11
                                floor_no = floor_no.split("/")[0]
                                orientation = item.get("face", "")  # 朝向
                                total_floor_num = re.findall("\d+", item.get("floor2", ""))
                                if total_floor_num:
                                    total_floor_num = total_floor_num[0]
                                else:
                                    total_floor_num = ''
                                area = item.get("distName")
                                publish_date = item.get("publishTime", "")[:10]  # 发布时间
                                cur_date = datetime.datetime.now()
                                if not any(["周边" in area, "旅游" in area, "风景" in area, "名胜" in area,
                                    "其他" in area, "其它" in area, "不限" in area, "周边" in area,
                                    (cur_date - datetime.datetime.strptime(publish_date, "%Y-%m-%d")).days > 31]):
                                    t_price = format_num(item.get("totalPrice"))  # 总价
                                    plot_name = item.get("haName", "")  # 楼盘名称
                                    project_code = item.get("haCode", "")
                                    address = item.get("address", "")  # 楼盘地址
                                    build_date = item.get("buildYear", "")  # 建筑年代
                                    gps = item.get("gps", "")  # gps信息  '39.47491160593571,116.30321709971135'

                                    dic_data = {"_id": guid,
                                                "list_page_url": sub_info["page_url"],
                                                "city": sub_info["city"],
                                                "title": title,
                                                "source_link": t_url,
                                                "data_source": sub_info["source"],
                                                "crt_time": str_crt_time,
                                                "house_structure": "",
                                                "project_alias": "",
                                                "inside_space": "",
                                                "usable_area": "",
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
                                                "area": area,
                                                "sub_area": "",
                                                "case_type_code": 3001001,
                                                "dealcode": dealcode,
                                                "project_code": project_code,
                                                "case_happen_date": publish_date,
                                                "gps": gps}
                                    data_list.append(dic_data)
                logger.info("已解析{}条数据{}".format(len(data_list), sub_info["page_url"]))
            try:
                next_href = content.xpath("string(//a[@class='pgdn']/@href)")
                if not next_href or not data_list:
                    flag = "finish"
                    logger.info("没有下一页{}".format(sub_info["page_url"]))
            except:
                logger.info("解析下一页异常{}".format(sub_info["page_url"]))

    dic_data = {"data": data_list, "flag": flag}
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
    crawling_model.logger.info("进入解析函数,{}".format(sub_info["page_url"]))
    try:
        pagesize = 50
        p_page = (re.findall(r'pg(\d*)', sub_info['page_url']) or ["1"])[0]  # p_page: list页的页码, 从1开始
        data_param = {
            "hacode": hacode,
            "pagesize": pagesize,
            "startnum": str(pagesize * page_index + 1),  # 用来控制请求数据的起始index
            "p[pagesize]": pagesize,
                "p[flag]": "1",
                'p[page]': p_page}
        url_param = "{}listnewajax.html".format(sub_info["sub_area_url"])
        # url_param="http://fz.cityhouse.cn/forsale/listnewajax.html"
        param_header = {
            'Referer': sub_info["page_url"],
            'Accept': 'Accept-Encoding:gzip, deflateAccept-Language:zh-CN,zh;q=0.8'}
        jdata = crawling_model.post(url_param, param_header, data_param)
        if jdata is None:
            dict_data = {}
        else:
            dict_data = json.loads(jdata) or {}
    except:
        dict_data = {}
        crawling_model.logger.error("post请求异常.{}".format(traceback.format_exc()))
    finally:
        return dict_data


if __name__ == '__main__':
    list_chengshifangchan("", "", "")
