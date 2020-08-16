import datetime
import queue
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError

from utils import common_mongo
from utils.common_downloader_detail import Downloader
from utils.common_err_detail import TypeSourceError
from concurrent.futures import ThreadPoolExecutor
import sys
import urllib3
import traceback
import random
from setting import config
from utils.common_logger import get_logger
from apps.fangtianxia import ftx_detail
from apps.tongcheng58 import tongcheng58_detail
from apps.cityhouse import cityhouse_detail
from apps.lianjia import lianjia_detail
from apps.anjuke import anjuke_detail
from hashlib import md5

from utils.common_mongo import MongoOption
from utils.constants import MIN_PERSISTENCE, CONTAINER_SIZE, INTERVAL_MAP, STOP_TIME, WARNING_TIME

urllib3.disable_warnings()
data_client = MongoOption()
container = queue.Queue(CONTAINER_SIZE)
downloader_container = queue.Queue(CONTAINER_SIZE)


# 获取表名
def table_name(base_table, idx):
    table = base_table + '_{}'.format(str(idx))
    if idx < 10:
        table = base_table + '_0{}'.format(str(idx))
    return table


# 获取表名
def table_name_by_city(base_table, city):
    return table_name(base_table, table_idx(city))


def table_idx(city):
    hash_code = int(md5(city.encode('UTF-8')).hexdigest(), 16)
    idx = hash_code % 50
    return idx


def crawl_spider(param):
    p_city = param[0]
    p_source = param[1]
    logger = get_logger(p_city, p_source, config.DETAIL_LOG_DIR)

    try:
        url_download = Downloader(logger, source)
        if p_source == '房天下租房':
            parse_str = ftx_detail.FangParse()
        elif p_source == '58同城租房':
            parse_str = tongcheng58_detail.Parse58()
        elif p_source == '城市房产租房':
            parse_str = cityhouse_detail.CityHouse()
        elif p_source == '安居客租房':
            parse_str = anjuke_detail.KeParse()
        elif p_source == '链家租房':
            parse_str = lianjia_detail.ParseLianJ()
        else:
            raise TypeSourceError

        time_num = 0
        get_item_num = 0
        less_than_50_num = 0
        while True:
            while True:
                if time_num <= 5:
                    try:
                        # time.sleep(random.randint(1, 30) / 10)
                        now_spider_time = (datetime.datetime.now() - datetime.timedelta(days=time_num))
                        gt_time = now_spider_time.strftime('%Y-%m-%d') + ' 00:00:00'
                        item_list = list(mongo.m_select({'city': p_city, 'd_status': {'$exists': False},
                                                         'data_source': p_source, 'crt_time': {'$gt': gt_time}},
                                                        'renting_case').skip(get_item_num*300).limit(300))
                        get_item_num += 1
                        if len(item_list) < 300:
                            get_item_num = 0
                        if not item_list:
                            item_list = list(mongo.m_select({'city': p_city, 'd_status': {'$exists': False},
                                                             'data_source': p_source, 'crt_time': {'$gt': gt_time}},
                                                            'renting_case').limit(300))
                        if len(item_list) < 50:
                            less_than_50_num += 1
                        else:
                            less_than_50_num = 0
                        if not item_list or less_than_50_num >= 5:
                            time_num += 1
                            get_item_num = 0
                            less_than_50_num = 0
                            # time.sleep(random.randint(3, 300))
                            continue
                        else:
                            break
                    except Exception as e:
                        print(e)
                        # time.sleep(random.randint(3, 300))
                        continue
                else:
                    item_list = []
                    break
            if len(item_list):
                logger.info("开启{}线程,共{}条case".format(p_city, len(item_list)))
                try:
                    for seen in item_list:
                        # print(seen['_id'])
                        url = seen['source_link']
                        coding = 'utf-8'
                        headers = {
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
                        if p_source == '房天下租房':
                            coding = 'gbk'
                            referer = 'http://search.fang.com/captcha-verify/redirect?h={}'.format(url)
                            # cookie = "global_cookie=858rxappvbibay2xvvj0knhnj2zjpdnfwnn; Integrateactivity=notincludemc; lastscanpage=0; newhouse_user_guid=8F79FB4C-E7E7-A82F-1EAB-80A740138AA1; budgetLayer=1%7Cbj%7C2019-06-18%2014%3A21%3A27; resourceDetail=1; searchConN=1_1562072520_529%5B%3A%7C%40%7C%3A%5Db2755e4c34cf6f19bdf36bf7f5e7f252; vh_newhouse=1_1562135369_1723%5B%3A%7C%40%7C%3A%5Dc986ba3e7921e9c51a1d863325527852; new_search_uid=6beab057a77eed00b3111dba591ed79b; __utmc=147393320; __utmz=147393320.1562934211.33.19.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/; Captcha=54424F47374E786264774E523870554A6C6367363442334A57532B4A676E6377487836486A496B66726B744E3739722B6D4F456C676A326F7342655A355A7346344B4B77335654306344303D; newhouse_chat_guid=43F0A0FB-EA25-9129-D97D-FC1C6A4025D1; city=sz; __utma=147393320.3500232.1560338584.1563071182.1563153028.35; g_sourcepage=esf_xq%5Elb_pc; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; unique_cookie=U_haxkax8249tj5zdl5h0tp1j9l1jjy02o0dx*44; __utmb=147393320.42.10.1563153028"
                            cookie = "global_cookie=nwv5jgfpbkuckdkwa0nxt3a2k17jztez4ee; city=shangrao; g_sourcepage=zf_fy%5Egrxq_pc; __utma=147393320.1531583592.1566885175.1568960980.1571189734.8; __utmc=147393320; __utmz=147393320.1571189734.8.8.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-091bbfcb470e0db82c/redirect; ASP.NET_SessionId=nj4a1e4fqs33ti5zbbdq3sp1; Rent_StatLog=42bb3892-6242-41e3-9705-5f64863f525a; unique_cookie=U_sc5spjnso1dhj4dw5hhx40r0526k1sloqsc*6; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.15.10.1571189734"
                            headers['referer'] = referer
                            headers["cookie"] = cookie
                        t1 = time.time()
                        result = url_download.get_str(url, headers=headers, encoding=coding)
                        t2 = time.time()
                        print(p_city,t2 - t1)

                        if result:
                            if any([
                                'captcha' in result['link'], 'verifycode' in result['link'], 'authcode' in result['link']]):
                                logger.warning('出现验证码！！！, the link is: \n' + result['link'])
                                # time.sleep(1)
                            else:
                                dic = parse_str.parse_xpath(result)
                                if dic:
                                    dic["_id"] = seen["_id"]
                                    container.put(UpdateOne({'_id': dic['_id']}, {'$set': dic}))
                                    if dic.get('d_status') == 'err':
                                        logger.info('parse  error')
                                else:
                                    logger.info('dic为空: ' + url)
                        else:
                            pass
                        process_cur_time = time.time()
                        if int(process_cur_time) - int(process_start_time) >= STOP_TIME:
                            save2db(0)
                            logger.info('{}进程已运行23个小时，退出程序'.format(p_city))
                            sys.exit()
                        time.sleep(random.randint(1, 10) / 10)
                        process_cur_time = time.time()
                        if int(process_cur_time) - int(process_start_time) >= STOP_TIME:
                            logger.info('{}进程已运行23个小时，退出程序'.format(p_city))
                            sys.exit()
                except Exception as e:
                    process_cur_time = time.time()
                    logger.error('craw err, {}, {}'.format(e, traceback.print_exc()))
                    if int(process_cur_time) - int(process_start_time) >= STOP_TIME:
                        save2db(0)
                        logger.info('{}进程已运行23个小时，退出程序'.format(p_city))
                        break
            else:
                save2db(0)
                logger.info('{}暂无数据，退出线程'.format(p_city))
                break
            # time.sleep(2)
            # time.sleep(300 / len(item_list))
    except Exception as e:
        logger.error('runing' + str(e))
        traceback.print_exc()

def save2db(min_persistence=MIN_PERSISTENCE):
    global data_client
    condition = []
    # time.sleep(1)
    public_logger.info("存储调度, 当前已爬取数据{}条".format(container.qsize()))
    if container.qsize() > min_persistence:
        try:
            for i in range(CONTAINER_SIZE):
                time.sleep(0.00001)
                if container.empty():
                    break
                else:
                    condition.append(container.get())
        except Exception as e:
            public_logger.error("准备数据异常{}, {}".format(e, traceback.format_exc()))
        else:
            if condition:
                try:
                    public_logger.info("准备入库{}条数据".format(len(condition)))
                    print("准备入库{}".format(len(condition)))
                    data_client.m_update(condition, "renting_case")
                    del condition[:]
                except BulkWriteError:
                    pass  # 存在数据重复的异常,忽略
                except Exception as e:
                    public_logger.error("存储数据库异常{},30s后重连".format(e))
                    # time.sleep(30)
                    time.sleep(10)
                    try:
                        data_client = MongoOption()
                    except Exception as e:
                        public_logger.info("重连数据库失败,{}".format(e))
                public_logger.info("完成入库...")


if __name__ == '__main__':

    print('pid:{}'.format(os.getpid()))
    if config.ENV == "dev":
        source = "城市房产租房"
        city_list = ["大连市","扬州市", "无锡市", "苏州市", "南京市", "盐城市", "常州市", '郑州市', "开封市", "商丘市", "许昌市", "平顶山市"]
        # city_list = ["郑州市", ]

    else:
        source = sys.argv[1]
        city_list = sys.argv[2:]
    # source = sys.argv[1]
    # city_list = sys.argv[2:]
    source = source.strip('" ')
    pool_num = len(city_list)
    print("city_list", city_list)
    mongo = common_mongo.MongoOption()
    public_logger = get_logger("public", source, config.DETAIL_LOG_DIR)
    scheduler = BackgroundScheduler()
    interval = INTERVAL_MAP[source] * 10 / pool_num
    scheduler.add_job(save2db, 'interval', seconds=interval)
    scheduler.start()
    pool_params = [(city.strip('" '), source) for city in city_list]
    process_start_time = time.time()
    if pool_num > 1:
        pool = ThreadPoolExecutor(max_workers=pool_num+1)
        pool.map(crawl_spider, pool_params)
        sys.exit()
    else:
        crawl_spider(pool_params[0])

