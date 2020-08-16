# -*- coding: utf-8 -*-
# @Time    : 19-4-21 下午4:53
# @Author  : luomingming


import logging
import re
import traceback
from datetime import datetime, timedelta

from FxtDataAcquisition.settings import *
from FxtDataAcquisition.utils.functions import *
from FxtDataAcquisition.utils.redis_client import rediz
from FxtDataAcquisition.service import distinct

logger = logging.getLogger(__name__)


def statis_list(item):
    statis(DAQ_LIST, item)


def statis_detail(item):
    statis(DAQ_DETAIL, item)


# statistics field loss num and increment num and total num
def statis(tp, item):
    key_pre = "{}@{}-".format(item['data_source'], item['city'])
    if tp == DAQ_LIST:
        name_incr = STATIS_LIST_INCR_KEY
        name = STATIS_LIST_KEY
        if not ('project_name' in item.keys()):
            rediz.hincrby(name_incr, key_pre + "project_name")
            rediz.hincrby(name, key_pre + "project_name")

        if not ('unitprice' in item.keys()):
            rediz.hincrby(name_incr, key_pre + "unitprice")
            rediz.hincrby(name, key_pre + "unitprice")

        if not ('house_area' in item.keys()):
            rediz.hincrby(name_incr, key_pre + "house_area")
            rediz.hincrby(name, key_pre + "house_area")
    else:
        name_incr = STATIS_DETAIL_INCR_KEY
        name = STATIS_DETAIL_KEY
    rediz.hincrby(name_incr, key_pre + "case_count")
    rediz.hincrby(name, key_pre + "case_count")


# 根据日期间隔计算案例时间
def compute_case_date(date_interval):
    is_last_month = False
    case_happen_date = None
    if '月前' in date_interval:
        is_last_month = True
    elif '天' in date_interval:
        try:
            interval = re.findall(r'\d+', date_interval)[0]
            case_happen_date = (datetime.now() - timedelta(days=int(interval))).strftime('%Y-%m-%d')
        except Exception as e:
            logger.error('{} compute date interval cased exception: {}'.format(datetime.now(), traceback.format_exc()))
    else:
        case_happen_date = datetime.now().strftime('%Y-%m-%d')

    return is_last_month, case_happen_date


def extract(node):
    return to_str(node.extract())


def get_full_city_name(city):
    city_f = distinct.city(city)
    if not city_f:
        city_f = city
    return city_f
