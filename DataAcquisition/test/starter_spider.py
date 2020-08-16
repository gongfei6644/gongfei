# -*- coding: utf-8 -*-
# @Time    : 2019-05-07 21:13
# @Author  : luomingming
# @Desc    :

import os
import time
import threading


def run(jobs):
    for job in jobs:
        os.system('scrapy crawl {} -a logfile=scrapy_{}.log'.format(job, job))


# 启动城市列表爬虫
def start_cities():
    print('启动城市列表爬虫')
    run(['fangtan_cities', 'house365_cities'])


# 启动案例列表爬虫
def start_list():
    print('启动案例列表爬虫')
    run(['fangtan_list', 'house365_list'])


# 启动案例详情爬虫
def start_detail():
    print('启动案例详情爬虫')
    run(['fangtan_detail', 'house365_detail'])


threading.Thread(target=start_cities).start()
time.sleep(60 * 10)

threading.Thread(target=start_list).start()
time.sleep(60 * 30)

threading.Thread(target=start_detail()).start()
