# -*- coding: utf-8 -*-
# @Desc    : 单价区间


import re

from app.config import CACHE_EX_TIME
from app.dbs.mysql_manager import mysql
from app.redis_util import conn

upr_pre = 'upricer_'


def put_cache(pre, upr):
    conn.pipeline().set(pre + upr[0], upr[1], ex=CACHE_EX_TIME).execute()


def unitprice_ranges():
    sql = 'SELECT city_name, unitprice_range FROM dat_unitprice_range;'
    lst = mysql.query(sql)
    for upr in lst:
        put_cache(upr_pre, upr)


unitprice_ranges()


def get_unitprice_range(city_name):
    sql = "SELECT city_name, unitprice_range FROM dat_unitprice_range WHERE city_name = '{}'".format(city_name)
    rt = mysql.query(sql)
    if rt:
        put_cache(upr_pre, rt[0])
        return rt[0][1]
    return None


# 校验单价区间
def valid_uprice_r(city_name, unitprice):
    upr = conn.get(upr_pre + city_name)
    if not upr:
        upr = get_unitprice_range(city_name)
    if upr:
        sp = upr.split('-')
        low = int(sp[0].strip())
        high = sp[1].strip()
        if high == '不限定':
            high = 9999999
        elif re.findall('[\u4e00-\u9fa5]', high):
            high = re.match('\d+', high).group()
        high = int(high)
        if unitprice < low or unitprice > high:
            return False
    return True
