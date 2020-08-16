# -*- coding: utf-8 -*-
# @Time    : 2018-12-20 10:24
# @Author  : luomingming
# @Desc    : 行政区服务, 该代码是从daq_std标准化项目拷贝过来的，
#            相关设置需与标准化项目保持一致，后续可做成公共服务以供调用。

from FxtDataAcquisition.utils.dbs.mysql_manager import mysql
from FxtDataAcquisition.utils.redis_client import rediz
from FxtDataAcquisition.settings import *

city_sql = """
select * from (
  select id, city_name, alias from sys_city where sys_status=1
  UNION ALL
  SELECT sys_id as id,sys_name as city_name,net_name as alias 
  FROM sys_comparision where status=1 and type=1
)t where 1=1
"""


def cities(_city=None):
    sql = city_sql
    if _city:
        sql = sql + " and (city_name='{}' or alias='{}')".format(_city, _city)
    lst = mysql.query(sql)
    for rs in lst:
        put_cache(CITY_PRE, rs)


def put_cache(pre, dist):
    rediz.pipeline() \
        .set(pre + dist[1], '{}:{}'.format(dist[1], dist[0]), ex=CACHE_EX_TIME) \
        .set(pre + dist[2], '{}:{}'.format(dist[1], dist[0]), ex=CACHE_EX_TIME) \
        .execute()


def city(param):
    key = '{}{}'.format(CITY_PRE, param)
    _city = rediz.get(key)
    if not _city:
        cities(param)
        _city = rediz.get(key)
    if _city:
        s = _city.split(":")
        return s[0]
    return None


def get_city_weights(_cities, source_pinyin):
    key = source_pinyin + "_" + CITY_WEIGHTS
    cws = rediz.get(key)
    if not cws:
        # sql = "SELECT GROUP_CONCAT(city_weight ORDER BY city_name) FROM sys_city_weight " \
        #       "WHERE city_name IN({})".format(_cities)
        # weights = ''.join(mysql.query(sql)[0])
        sql = "SELECT city_name, city_weight FROM sys_city_weight " \
              "WHERE city_name IN({}) ORDER BY city_name".format(_cities)
        lst = mysql.query(sql)
        if lst:
            c_str = ''
            w_str = ''
            for cw in lst:
                c_str += str(cw[0]) + ','
                w_str += str(cw[1]) + ','
            c_str = c_str.rstrip(',')
            w_str = w_str.rstrip(',')
            cws = c_str + ":" + w_str
            rediz.set(key, cws, CACHE_EX_TIME)
    return cws
