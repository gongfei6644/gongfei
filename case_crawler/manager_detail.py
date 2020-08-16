import datetime
import re
import time
import os

from pymongo import UpdateOne
from utils import common_mongo, common_mq
from utils.common_downloader_detail import product_download, test_product_download, test2_product_download
from utils.common_err_detail import TypeSourceError
from concurrent.futures import ThreadPoolExecutor
import sys
import urllib3
import traceback
import random
from setting import config
from utils.common_logger import get_logger
from apps.fangtianxia import ftx_detail
from apps.fangchanchaoshi import fangchanstore_detail
from apps.tongcheng58 import tongcheng58_detail
from apps.zhongyuandichan import zhongyuan_detail
from apps.cityhouse import cityhouse_detail
from apps.ganjiwang import ganji_detail
from apps.lianjia import lianjia_detail
from apps.anjuke import anjuke_detail
from apps.zhugezhaofang import zhuge_detail
from hashlib import md5

secret = "f717e1badb"

urllib3.disable_warnings()


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
    global secret
    p_city = param[0]
    p_source = param[1]

    try:
        logger = get_logger(p_city, p_source, config.DETAIL_LOG_DIR)

        total = 0
        num = 0
        start_time = time.time()

        url_download = product_download(logger)
        if p_source == '房天下二手房':
            parse_str = ftx_detail.FangParse()
            url_download = test_product_download(logger)
        elif p_source == '58同城二手房':
            parse_str = tongcheng58_detail.Parse58()
        elif p_source == '城市房产二手房':
            parse_str = cityhouse_detail.CityHouse()
        elif p_source == '赶集网二手房':
            parse_str = ganji_detail.ParseGanji()
        elif p_source == '安居客二手房':
            parse_str = anjuke_detail.KeParse()
            url_download = test2_product_download(logger)
        elif p_source == '链家二手房':
            parse_str = lianjia_detail.ParseLianJ()
        elif p_source == '诸葛找房二手房':
            parse_str = zhuge_detail.ParseZhuge()
        elif p_source == '中原地产二手房':
            parse_str = zhongyuan_detail.ParseZy()
        elif p_source == '中国房产超市二手房':
            parse_str = fangchanstore_detail.ParseFangStore()
        else:
            raise TypeSourceError

        while True:
            table_name = table_name_by_city('Dat_case', p_city)
            print(table_name)
            time_num = 0
            while True:
                if time_num <= 5:
            # gt_time = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min).strftime('%Y-%m-%d %H:%M:%S')
                    try:
                        now_spider_time = (datetime.datetime.now() - datetime.timedelta(days=time_num)).strftime('%Y-%m-%d')
                        gt_time = now_spider_time + ' 00:00:00'
                        print(gt_time)
                        item_list = list(mongo.m_select({'city': p_city, 'd_status': {'$exists': False},
                                                         'data_source': p_source, 'crt_time': {'$gt': gt_time}}, table_name).limit(1200))
                        if not item_list:
                            time_num += 1
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
                    result_list = []
                    for seen in item_list:
                        url = seen['source_link']
                        coding = 'utf-8'
                        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
                        if p_source == '中国房产超市二手房':
                            coding = 'gbk'

                        if p_source == '房天下二手房':
                            referer = 'http://search.fang.com/captcha-{}/redirect?h={}'.format(secret, url)
                            cookie = "global_cookie=858rxappvbibay2xvvj0knhnj2zjpdnfwnn; Integrateactivity=notincludemc; lastscanpage=0; newhouse_user_guid=8F79FB4C-E7E7-A82F-1EAB-80A740138AA1; budgetLayer=1%7Cbj%7C2019-06-18%2014%3A21%3A27; resourceDetail=1; searchConN=1_1562072520_529%5B%3A%7C%40%7C%3A%5Db2755e4c34cf6f19bdf36bf7f5e7f252; vh_newhouse=1_1562135369_1723%5B%3A%7C%40%7C%3A%5Dc986ba3e7921e9c51a1d863325527852; new_search_uid=6beab057a77eed00b3111dba591ed79b; __utmc=147393320; __utmz=147393320.1562934211.33.19.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/; Captcha=54424F47374E786264774E523870554A6C6367363442334A57532B4A676E6377487836486A496B66726B744E3739722B6D4F456C676A326F7342655A355A7346344B4B77335654306344303D; newhouse_chat_guid=43F0A0FB-EA25-9129-D97D-FC1C6A4025D1; city=sz; __utma=147393320.3500232.1560338584.1563071182.1563153028.35; g_sourcepage=esf_xq%5Elb_pc; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; unique_cookie=U_haxkax8249tj5zdl5h0tp1j9l1jjy02o0dx*44; __utmb=147393320.42.10.1563153028"
                            headers['referer'] = referer
                            headers["cookie"] = cookie
                            headers["Cache-Control"] = "no-cache"


                        if p_source == '诸葛找房二手房':
                            host = url[8:].split("/")[0] if url.startswith("https") else url[7:].split("/")[0]
                            headers['Host'] = host
                            headers["Accept-Language"] = 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'

                        result = url_download.get_str(url, headers=headers, encoding=coding)
                        '''
                            "User-Agent": "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)",
                            "Host": host,
                            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
                        '''

                        if result:
                            if 'captcha' not in result['link'] and 'verifycode' not in result['link'] and 'authcode' not in result['link']:
                                dic = parse_str.parse_xpath(result)
                                print(dic)
                                if dic:
                                    dic["_id"] = seen["_id"]
                                    result_list.append(dic)
                                    if dic.get('d_status') == 'err':
                                        logger.info('parse  error')
                                    num += 1
                                    total += 1
                                else:
                                    logger.info('dic为空: ' + url)
                            else:
                                if p_source == "房天下二手房":
                                    try:
                                        resp = url_download.get_str(url)
                                        captcha_url = resp["link"]
                                        secret = re.findall(r'/captcha-(.+)/', captcha_url, re.S)[0]
                                        print("secret", secret)

                                    except:
                                        logger.warning('检查验证码:\n{}'.format(result['link']))
                                time.sleep(3)
                        else:
                            pass
                        cur_time = time.time()
                        if int(cur_time) - int(start_time) >= 3600:
                            logger.info('程序运行1个小时，准备发送消息--{}'.format(p_city))
                            params = {'add_case_count': num, 'add_lsprojectname_count': -1, 'add_lsbuildarea_count': -1,
                                      'add_lsunitprice_count': -1}

                            common_mq.send_mq_msg('increase', 'details', p_city, p_source, params)
                            logger.info('the message send: \n' + str(params))
                            start_time = cur_time
                            num = 0
                        process_cur_time = time.time()
                        if int(process_cur_time) - int(process_start_time) >= 82800:
                            condition_list = [
                                UpdateOne({'_id': case['_id']}, {'$set': case}, upsert=True) for case in result_list]
                            if condition_list:
                                mongo.m_update(condition_list, table_name)  # 可传入第二个参数为表名,用来测试
                                logger.info('{}进程已运行23个小时，准备退出-----插入数据: {}条案例'.format(p_city, len(condition_list)))
                            logger.info('{}进程已运行23个小时，退出程序'.format(p_city))
                            sys.exit()
                        time.sleep(random.randint(1, 30) / 10)
                    condition_list = [
                        UpdateOne({'_id': case['_id']}, {'$set': case}, upsert=True) for case in result_list]
                    if condition_list:
                        mongo.m_update(condition_list, table_name)  # 可传入第二个参数为表名,用来测试
                        logger.info('插入完成: {}条案例'.format(len(condition_list)))

                        cur_time = time.time()
                        if int(cur_time) - int(start_time) >= 3600:
                            logger.info('程序运行1个小时，准备发送消息--{}'.format(p_city))
                            params = {'add_case_count': num, 'add_lsprojectname_count': -1, 'add_lsbuildarea_count': -1,
                                      'add_lsunitprice_count': -1}

                            common_mq.send_mq_msg('increase', 'details', p_city, p_source, params)
                            logger.info('the message send: \n' + str(params))
                            start_time = cur_time
                            num = 0
                        process_cur_time = time.time()
                        if int(process_cur_time) - int(process_start_time) >= 82800:
                            logger.info('{}进程已运行23个小时，退出程序'.format(p_city))
                            sys.exit()
                except Exception as e:
                    # print('crawl', e)
                    logger.error('crawerr, {}, {}'.format(e, traceback.print_exc()))
                    cur_time = time.time()
                    if int(cur_time) - int(start_time) >= 3600:
                        logger.info('程序运行1个小时，准备发送消息--{}'.format(p_city))
                        params = {'add_case_count': num, 'add_lsprojectname_count': -1, 'add_lsbuildarea_count': -1,}
                        common_mq.send_mq_msg('increase', 'details', p_city, p_source, params)
                        logger.info('the message send: \n' + str(params))
                        start_time = cur_time
                        num = 0
                    process_cur_time = time.time()
                    if int(process_cur_time) - int(process_start_time) >= 82800:
                        logger.info('{}进程已运行23个小时，退出程序'.format(p_city))
                        break
            else:
                logger.info('{}暂无数据，退出线程'.format(p_city))
                params = {'case_count': total, 'lsunitprice_count': -1, 'lsbuildarea_count': -1, 'lsprojectname_count': -1}
                common_mq.send_mq_msg('total', 'details', p_city, p_source, params)
                break
            time.sleep(3)
            time.sleep(360/len(item_list))
    except Exception as e:
        logger.error('runing' + str(e))
        traceback.print_exc()


if __name__ == '__main__':

    print('pid:{}'.format(os.getpid()))
    if config.ENV == "dev":
        source = "房天下二手房"
        city_list = ["北京市"]
        # city_list = ["北京市", "上海市", "深圳市"]
    else:
        source = sys.argv[1]
        city_list = sys.argv[2:]
    # source = sys.argv[1]
    # city_list = sys.argv[2:]
    source = source.strip('" ')
    pool_num = len(city_list)
    mongo = common_mongo.MongoOption()
    pool_params = [(city.strip('" '), source) for city in city_list]
    # exit()
    process_start_time = time.time()
    if pool_num > 1:
        pool = ThreadPoolExecutor(max_workers=pool_num)
        pool.map(crawl_spider, pool_params)
        sys.exit()
    else:
        crawl_spider(pool_params[0])

    # 启动命令: python manager_detail.py 诸葛找房二手房 温州市 广州市 福州市
    # GLUE: python3 /usr/local/DataCollection/fxt_case_crawler/manager_detail.py $1

