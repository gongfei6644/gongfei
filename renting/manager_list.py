# coding=utf-8

"""
入口文件
"""
import os
import queue
import sys
import copy
import time
import datetime
import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from lxml import etree
from pymongo import InsertOne
from pymongo.errors import BulkWriteError
from concurrent.futures import ThreadPoolExecutor
from utils.common_mongo import MongoOption

from setting import config
from utils.common_mq import send_mq_msg
from utils.common_logger import get_logger
from utils.common_tools import make_urls
from utils.common_downloader_list import crawling
from apps.fangtianxia.fangtianxia_list import list_fangtianxia
from apps.lianjia.lianjia_list import list_lianjia
from apps.tongcheng58.tongcheng58_list import list_58tongcheng
from apps.anjuke.anjuke_list import list_anjuke
from apps.cityhouse.cityhouse_list import list_chengshifangchan
from utils.constants import (STOP_TIME, WARNING_TIME, CONTAINER_SIZE, INTERVAL_MAP, MIN_PERSISTENCE)

PARSE_MAP = {
    "链家租房": list_lianjia,
    "58同城租房": list_58tongcheng,
    "安居客租房": list_anjuke,
    "房天下租房": list_fangtianxia,
    "城市房产租房": list_chengshifangchan,
    }

data_client = MongoOption()
container = queue.Queue(CONTAINER_SIZE)

def get_morecity_bycitylist(param_city):
    """
    按城市查询城市下的所有片区同步采集
    :param param_city:source和city_name参数的元组
    """
    source, city_name = param_city

    logger = get_logger(city_name, source, config.LIST_LOG_DIR)
    try:
        city_info = data_client.get_config(city_name, source) or []
        logger.info("{}片区{}个".format(city_name, len(city_info)))

    except Exception as e:
        logger.error("查询数据库config表异常:{},{}".format(e, traceback.format_exc()))
    else:
        crawling_model = crawling(source, logger)
        # 初始化统计数据
        dic_static = {"case_count": 0,
                      "lsproject_count": 0,
                      "lsunitprie_count": 0,
                      "lsbuildarea_count": 0,
                      "add_case_count": 0,
                      "add_lsproject_count": 0,
                      "add_lsunitprie_count": 0,
                      "add_lsbuildarea_count": 0,
                      "flag": "normal",
                      "run_time": int(time.time())
                      }

        logger.info("开始析取{}{}列表数据".format(source, city_name))
        for item in city_info:
            page_urls = make_urls(item)
            dic_static["flag"] = "normal"
            for page_url in page_urls:
                if int(time.time()) - process_start_time >= STOP_TIME:
                    logger.info('{}进程已运行23个小时，退出程序'.format(city_name))
                    return
                flag = dic_static.get("flag", "normal")
                if flag != "normal":  # 状态为完成, 停止翻页
                    break
                else:  # 进入下载解析存储流程
                    sub_info = copy.deepcopy(item)
                    sub_info["page_url"] = page_url
                    dic_static = parse_list_page(logger, crawling_model, dic_static, sub_info)

        logger.info("完成析取{}{}列表数据时间:{}".format(source, city_name, str(datetime.datetime.now())))

        # 全部采集完发送全量的消息
        # send_mq_msg("total", "list", city_name, source, dic_static)
        # 记录消息日志
        logger.info(
            "发送全量数据：{},{},{},{},case_count={},projectname_count={},unitprice_count={},buildarea_count={}".format(
                "total", "list", city_name, source,
                dic_static.get("case_count", 0),
                dic_static.get("lsproject_count", 0),
                dic_static.get("lsunitprie_count", 0),
                dic_static.get("lsbuildarea_count", 0)
            ))
    save2db(0)


def parse_list_page(logger, crawling_model, dic_static, sub_info):
    """
    下载,解析, 入库
    :param logger: 日志管理器
    :param crawling_model:下载器
    :param dic_static: 统计数据
    :param sub_info: 片区信息
    :return:
    """
    global data_client

    if int(time.time()) - process_start_time >= STOP_TIME:
        return
    # 定时发消息
    if int(time.time()) - dic_static["run_time"] >= WARNING_TIME:
        # send_mq_msg("increase", "list", sub_info["city"], sub_info["source"], dic_static)
        logger.info(
            "发送预警消息：messagetype={},collecttype={},cityname={},source={},dic_static={}".format(
                "increase", "list", sub_info["city"], sub_info["source"], dic_static))

        # 重置增量值
        dic_static["add_case_count"] = 0
        dic_static["add_lsbuildarea_count"] = 0
        dic_static["add_lsunitprie_count"] = 0
        dic_static["add_lsproject_count"] = 0
        dic_static["run_time"] = int(time.time())
    encoding = 'gbk' if sub_info["source"] in {"房天下租房", "中国房产超市租房"} else "utf-8"
    headers = {}
    if sub_info["source"] == "诸葛找房租房":
        length = 8 if sub_info["page_url"].startswith("https") else 7
        headers = {
            'Accept-Language': 'en-US,en:q=0.9,zh-CN:q=0.8,zh:q=0.7',
            "Host": sub_info["page_url"][length:].split("/")[0]}

    # elif sub_info["source"] == "城市房产租房":
    #     headers = {'Accept': 'Accept-Encoding:gzip, deflateAccept-Language:zh-CN,zh;q=0.8',
    #                'referer': sub_info['page_url'],
                   # 'Cookie': 'cityre=87492c6ee80bd7e84d010c75fd079d88; = 1570952311;Hm_lpvt_435bf6d47bee0643980454513deeb34f = 1570952311',
                   # 'User-Agent': "Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                   # }
    # elif sub_info["source"] == "房天下租房":
    #     referer = "http://search.fang.com/captcha-verify/redirect?h={}".format(sub_info["page_url"])
    #     cookie = "global_cookie=858rxappvbibay2xvvj0knhnj2zjpdnfwnn; Integrateactivity=notincludemc; lastscanpage=0; newhouse_user_guid=8F79FB4C-E7E7-A82F-1EAB-80A740138AA1; searchConN=1_1562072520_529%5B%3A%7C%40%7C%3A%5Db2755e4c34cf6f19bdf36bf7f5e7f252; vh_newhouse=1_1562135369_1723%5B%3A%7C%40%7C%3A%5Dc986ba3e7921e9c51a1d863325527852; new_search_uid=6beab057a77eed00b3111dba591ed79b; integratecover=1; __utmc=147393320; newhouse_chat_guid=F338123B-36B6-B946-6D33-B9BEDD74088F; keyWord_recenthouseaba=%5b%7b%22name%22%3a%22%e5%a3%a4%e5%a1%98%e5%8e%bf%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a013524%2f%22%2c%22sort%22%3a1%7d%5d; keyWord_recenthouseakesu=%5b%7b%22name%22%3a%22%e9%98%bf%e5%85%8b%e8%8b%8f%e5%b8%82%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a013308%2f%22%2c%22sort%22%3a1%7d%5d; keyWord_recenthousezz=%5b%7b%22name%22%3a%22%e9%87%91%e6%b0%b4%e5%8c%ba%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a0362%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e5%af%8c%e7%94%b0%e5%a4%a7%e5%8e%a6%22%2c%22detailName%22%3a%22%e9%87%91%e6%b0%b4%e5%8c%ba%22%2c%22url%22%3a%22%2fhouse-a0362-b04543%2f%22%2c%22sort%22%3a2%7d%5d; keyWord_recenthousesh=%5b%7b%22name%22%3a%22%e9%9d%99%e5%ae%89%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a021%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e5%8d%97%e4%ba%ac%e8%a5%bf%e8%b7%af%22%2c%22detailName%22%3a%22%e9%9d%99%e5%ae%89%22%2c%22url%22%3a%22%2fhouse-a021-b01623%2f%22%2c%22sort%22%3a2%7d%5d; Rent_StatLog=dac051f3-2f97-4739-b401-dc504f65fc21; keyWord_recenthousebj=%5b%7b%22name%22%3a%22%e6%9c%9d%e9%98%b3%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a01%2fh350%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e5%a5%a5%e6%9e%97%e5%8c%b9%e5%85%8b%e5%85%ac%e5%9b%ad%22%2c%22detailName%22%3a%22%e6%9c%9d%e9%98%b3%22%2c%22url%22%3a%22%2fhouse-a01-b02652%2fh350%2f%22%2c%22sort%22%3a2%7d%2c%7b%22name%22%3a%22CBD%22%2c%22detailName%22%3a%22%e6%9c%9d%e9%98%b3%22%2c%22url%22%3a%22%2fhouse-a01-b05510%2fh31-i350%2f%22%2c%22sort%22%3a2%7d%5d; keyWord_recenthousely=%5b%7b%22name%22%3a%22%e9%ab%98%e6%96%b0%22%2c%22detailName%22%3a%22%e6%b6%a7%e8%a5%bf%e5%8c%ba%22%2c%22url%22%3a%22%2fhouse-a010204-b012374%2fh31%2f%22%2c%22sort%22%3a2%7d%5d; __utma=147393320.1504671198.1563161384.1564038187.1564103717.15; __utmz=147393320.1564103717.15.11.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; city=ly; g_sourcepage=zf_fy%5Elb_pc; ASP.NET_SessionId=3lxrim4ydfq2welakqlme3rx; unique_cookie=U_h9ltwhyjfb0i30sq7dacdbqov1pjye39uzw*147; Captcha=667370653855576D5055674779706535414B783149554A6744382F3348333448505266706659466137332F417557444E484F367A71474B5546484D394A345545326E313050664D544548673D; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.9.10.1564103717"
    #     headers = {
    #         "cache-control": "no-cache",
    #         "referer": referer,
    #         "cookie": cookie,
    #     }
    if config.PROXY == "aby":
        if  sub_info["source"] == "Q房网租房": # sub_info["source"] == "城市房产租房" or
            content = crawling_model.get_by_chrome(sub_info["page_url"])
        else:
            content = crawling_model.get_by_abucloud(sub_info["page_url"], headers, encoding=encoding)
    else:
        content = crawling_model.get(sub_info["page_url"], sub_info["source"], encoding=encoding)
    if content == "retry":
        logger.info("下载页面失败.{}".format(sub_info["page_url"]))
    elif not content:
        pass
    else:
        parse_function = PARSE_MAP[sub_info["source"]]
        dic_data = parse_function(logger, content, sub_info)
        data_list = dic_data.get("data")
        logger.info("成功解析{}条数据{}".format(len(data_list), sub_info["page_url"]))
        if data_list:
            for data in data_list:

                dic_static["case_count"] += 1  # 采集总数
                dic_static["add_case_count"] += 1  # 递增的采集量

                if not data.get("project_name"):
                    dic_static["lsproject_count"] += 1
                    dic_static["add_lsproject_count"] += 1

                if not data.get('unitprice'):
                    dic_static["lsunitprie_count"] += 1
                    dic_static["add_lsunitprie_count"] += 1

                if not data.get('house_area'):
                    dic_static["lsbuildarea_count"] += 1
                    dic_static["add_lsbuildarea_count"] += 1
                # 加入缓存队列
                if container.qsize() < CONTAINER_SIZE and sub_info["source"] != "城市房产租房":
                    container.put(data)
            if sub_info["source"] == "城市房产租房":
                try:
                    condition = [InsertOne(data) for data in data_list]
                    public_logger.info("准备入库{}条数据".format(len(condition)))
                    print("准备入库{}".format(len(condition)))
                    data_client.m_insert(condition, "renting_case")
                    time.sleep(5)
                except BulkWriteError:
                    pass  # 存在数据重复的异常,忽略
                except Exception as e:
                    logger.error("存储数据库异常{}{},30s后重连".format(e, traceback.format_exc()))
                    time.sleep(30)
                    try:
                        data_client = MongoOption()
                        condition = [InsertOne(data) for data in data_list]
                        data_client.m_insert(condition, "renting_case")
                    except Exception as e:
                        logger.info("重连数据库失败,{}".format(e))

                logger.info("完成入库,{}".format(sub_info["page_url"]))
        dic_static["flag"] = dic_data["flag"]

    return dic_static


def save2db(min_persistence=MIN_PERSISTENCE):
    global data_client
    condition = []
    time.sleep(1)
    if container.qsize() > min_persistence:
        try:
            for i in range(CONTAINER_SIZE):
                time.sleep(0.00001)
                if container.empty():
                    break
                else:
                    condition.append(InsertOne(container.get()))
        except Exception as e:
            public_logger.error("准备数据异常{}, {}".format(e, traceback.format_exc()))
        else:
            if condition:
                try:
                    public_logger.info("准备入库{}条数据".format(len(condition)))
                    print("准备入库{}".format(len(condition)))
                    data_client.m_insert(condition, "renting_case")
                    del condition[:]
                except BulkWriteError:
                    pass  # 存在数据重复的异常,忽略
                except Exception as e:
                    public_logger.error("存储数据库异常{},30s后重连".format(e))
                    time.sleep(300)
                    try:
                        data_client = MongoOption()
                    except Exception as e:
                        public_logger.info("重连数据库失败,{}".format(e))
                public_logger.info("完成入库...")



if __name__ == "__main__":
    process_start_time = int(time.time())
    print('pid:{}'.format(os.getpid()))

    if config.ENV == "dev":
        source = "城市房产租房"
        city_list = ["扬州市",  "无锡市", "苏州市", "南京市", "盐城市", "常州市",'郑州市',"开封市","商丘市","许昌市","平顶山市"]
        # city_list = ["郑州市", "开封市", "洛阳市", "平顶山市", "焦作市", "鹤壁市", "新乡市", "安阳市", "濮阳市",
        #              "许昌市", "漯河市", "三门峡市", "南阳市", "商丘市", "信阳市", "周口市", "驻马店市", "济源市"]
    else:
        source = sys.argv[1].strip('" ')
        city_list = sys.argv[2:]
        city_list = [city.strip('" ') for city in city_list]
        # source = "58同城租房"
        # city_list = ["郑州市", "开封市", "洛阳市", "平顶山市", "焦作市", "鹤壁市", "新乡市", "安阳市", "濮阳市",
        #              "许昌市", "漯河市", "三门峡市", "南阳市", "商丘市", "信阳市", "周口市", "驻马店市", "济源市"]

    t_num = len(city_list)
    public_logger = get_logger("public", source, config.LIST_LOG_DIR)
    public_logger.info("{}启动任务:{}".format(source, city_list))
    scheduler = BackgroundScheduler()
    interval = INTERVAL_MAP[source] * 5/t_num
    scheduler.add_job(save2db, 'interval', seconds=interval)
    scheduler.start()
    if t_num == 1:
        get_morecity_bycitylist((source, city_list[0]))
    else:
        param_list = [(source, city.strip('" ')) for city in city_list]
        with ThreadPoolExecutor(max_workers=t_num) as pool:
            pool.map(get_morecity_bycitylist, param_list)
    time.sleep(30)
