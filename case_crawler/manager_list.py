# coding=utf-8

"""
入口文件
"""
import base64
import os
import sys
import copy
import time
import datetime
import traceback
from threading import RLock
from urllib.parse import quote

from apscheduler.schedulers.background import BackgroundScheduler
from lxml import etree
from pymongo import InsertOne
from pymongo.errors import BulkWriteError
from concurrent.futures import ThreadPoolExecutor
from utils.common_mongo import MongoOption

from setting import config
from utils.common_mq import send_mq_msg
from utils.common_logger_list import get_logger
from utils.common_tools import make_urls
from utils.common_downloader_list import crawling
from apps.fangchanchaoshi.fangchanchaoshi_list import list_fangchanchaoshi
from apps.fangtianxia.fangtianxia_list import list_fangtianxia
from apps.lianjia.lianjia_list import list_lianjia
from apps.tongcheng58.tongcheng58_list import list_58tongcheng
from apps.anjuke.anjuke_list import list_anjuke
from apps.ganjiwang.ganji_list import list_ganji
from apps.qfangwang.qfang_list import list_qfang
from apps.zhongyuandichan.zhongyuan_list import list_zhongyuandichan
from apps.zhugezhaofang.zhuge_list import list_zhugezhaofang
from apps.cityhouse.chengshifangchan_list import list_chengshifangchan
from utils.constants import (STOP_TIME, WARNING_TIME, CONTAINER_SIZE, INTERVAL_MAP, MIN_PERSISTENCE, INTERVAL,
                             LIST_SIZE)
from utils.switch_table import table_name_by_city

PARSE_MAP = {
    "Q房网二手房": list_qfang,
    "赶集网二手房": list_ganji,
    "链家二手房": list_lianjia,
    "58同城二手房": list_58tongcheng,
    "安居客二手房": list_anjuke,
    "房天下二手房": list_fangtianxia,
    "诸葛找房二手房": list_zhugezhaofang,
    "中原地产二手房": list_zhongyuandichan,
    "中国房产超市二手房": list_fangchanchaoshi,
    "城市房产二手房": list_chengshifangchan,
    }

data_client = MongoOption()
container = {}

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
        send_mq_msg("total", "list", city_name, source, dic_static)
        # 记录消息日志
        logger.info(
            "发送全量数据：{},{},{},{},case_count={},projectname_count={},unitprice_count={},buildarea_count={}".format(
                "total", "list", city_name, source,
                dic_static.get("case_count", 0),
                dic_static.get("lsproject_count", 0),
                dic_static.get("lsunitprie_count", 0),
                dic_static.get("lsbuildarea_count", 0)
            ))
    # save2db(0)  # 线程退出时存储一次


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
        send_mq_msg("increase", "list", sub_info["city"], sub_info["source"], dic_static)
        logger.info(
            "发送预警消息：messagetype={},collecttype={},cityname={},source={},dic_static={}".format(
                "increase", "list", sub_info["city"], sub_info["source"], dic_static))

        # 重置增量值
        dic_static["add_case_count"] = 0
        dic_static["add_lsbuildarea_count"] = 0
        dic_static["add_lsunitprie_count"] = 0
        dic_static["add_lsproject_count"] = 0
        dic_static["run_time"] = int(time.time())
    encoding = 'gbk' if sub_info["source"] in {"房天下二手房", "中国房产超市二手房"} else "utf-8"
    headers = {}
    if sub_info["source"] == "诸葛找房二手房":
        length = 8 if sub_info["page_url"].startswith("https") else 7
        headers = {
            'Accept-Language': 'en-US,en:q=0.9,zh-CN:q=0.8,zh:q=0.7',
            "Host": sub_info["page_url"][length:].split("/")[0]}

    elif sub_info["source"] == "城市房产二手房":
        headers = {'Accept': 'Accept-Encoding:gzip, deflateAccept-Language:zh-CN,zh;q=0.8'}
    elif sub_info["source"] == "房天下二手房":
        # burl = base64.b64encode(sub_info["page_url"].encode("gb2312"))
        # uurl = quote(burl)
        # referer = "http://search.fang.com/captcha-verify/redirect?h={}".format(uurl)
        headers = {
            "cache-control": "no-cache",
            'referer': "http://search.fang.com/captcha-verify/redirect?h={}".format(sub_info["page_url"]),
        "cookie": "global_cookie=d5k6rno67xtmcuhtfdo5hyf6k17jto5htlm; Integrateactivity=notincludemc; lastscanpage=0; resourceDetail=1; newhouse_user_guid=D85C6C91-2816-BD85-1F86-70A8AA3EAEC3; SKHRecordsbj=%25e5%25be%25a1%25e6%25b1%25a4%25e5%25b1%25b1%257c%255e2019%252f7%252f10%2b0%253a56%253a03%257c%255e0; __utmc=147393320; logGuid=29d640d6-ef9c-49bc-86c4-31cf513f0f75; g_sourcepage=ehlist; city=sz; __utma=147393320.470917304.1559313918.1563070350.1563074470.8; __utmz=147393320.1563074470.8.6.utmcsr=esf.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/house-a013/h314; __utmb=147393320.12.10.1563074470; unique_cookie=U_yd47zws6q9eh0w8bcy8fys9xk28jy2bq8vt*18",

        }
    if config.PROXY == "aby":
        if sub_info["source"] == "Q房网二手房":
            content = crawling_model.get_by_chrome(sub_info["page_url"])
        else:
            content = crawling_model.get_by_abucloud(sub_info["page_url"], headers, encoding=encoding)
    else:
        content = crawling_model.get(sub_info["page_url"], sub_info["source"], encoding=encoding)
    if content == "retry":
        logger.info("下载页面失败.{}".format(sub_info["page_url"]))
    else:
        html = etree.HTML(content)
        parse_function = PARSE_MAP[sub_info["source"]]
        dic_data = parse_function(logger, html, sub_info)
        data_list = dic_data.get("data")
        logger.info("成功解析{}条数据{}".format(len(data_list), sub_info["page_url"]))
        if data_list:
            key = table_name_by_city(data_list[0]["city"])
            if not container.get(key):
                container[key] = []
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
                # 加入缓存列表
                if len(container[key]) < LIST_SIZE and source != "城市房产二手房":
                    container[key].append(data)
            if source == "城市房产二手房":
                    try:
                        condition = [InsertOne(data) for data in data_list]
                        logger.info("准备入库{}条数据".format(len(condition)))
                        print("准备入库{}".format(len(condition)))
                        data_client.m_insert(condition, key)
                        time.sleep(5)
                    except BulkWriteError:
                        pass  # 存在数据重复的异常,忽略
                    except Exception as e:
                        logger.error("存储数据库异常{}{},30s后重连".format(e, traceback.format_exc()))
                        time.sleep(30)
                        try:
                            data_client = MongoOption()
                        except Exception as e:
                            logger.info("重连数据库失败,{}".format(e))

                    logger.info("完成入库,{}".format(sub_info["page_url"]))



        dic_static["flag"] = dic_data["flag"]

    return dic_static

def save2db():
    global data_client
    public_logger.info("准备入库...")
    with RLock():
        for k, v in container.items():
            if v:
                condition = [InsertOne(d) for d in v]
                try:
                    public_logger.info("{}入库,{}条数据".format(k, len(condition)))
                    print("{}入库{}条数据".format(k, len(condition)))
                    data_client.m_insert(condition, k)
                    # del condition[:]
                except BulkWriteError:
                    pass  # 存在数据重复的异常,忽略
                except Exception as e:
                    public_logger.error("插入数据库异常{}".format(e))
                except Exception as e:
                    public_logger.error("存储数据库异常{},30s后重连".format(e))
                    time.sleep(60)
                    try:
                        data_client = MongoOption()
                    except Exception as e:
                        public_logger.info("重连数据库失败,{}".format(e))
                container[k] = []
    public_logger.info("完成入库...")



if __name__ == "__main__":
    process_start_time = int(time.time())
    print('pid:{}'.format(os.getpid()))

    if config.ENV == "dev":
        source = "房天下二手房"
        city_list = ["北京市"]
        # city_list = ["上海市", "深圳市"]
    else:
        source = sys.argv[1].strip('" ')
        city_list = sys.argv[2:]
        city_list = [city.strip('" ') for city in city_list]
    t_num = len(city_list)
    public_logger = get_logger("public", source, config.LIST_LOG_DIR)
    public_logger.info("{}启动任务:{}".format(source, city_list))
    scheduler = BackgroundScheduler()

    scheduler.add_job(save2db, 'interval', seconds=INTERVAL_MAP[source])
    scheduler.start()
    if t_num == 1:
        get_morecity_bycitylist((source, city_list[0]))
    else:
        param_list = [(source, city.strip('" ')) for city in city_list]
        with ThreadPoolExecutor(max_workers=t_num) as pool:
            pool.map(get_morecity_bycitylist, param_list)
    time.sleep(30)


