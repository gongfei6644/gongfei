# -*- coding: utf-8 -*-
# @Desc    : 行政区服务

from app.config import *
from app.redis_util import conn
from ..dbs.mysql_manager import mysql
from app.service.sqls.district_sql import *


def cities(_city=None):
    sql = city_sql
    if _city:
        sql = sql + " and (city_name='{}' or alias='{}')".format(_city, _city)
    lst = mysql.query(sql)
    for rs in lst:
        # rs : (id,city_name,alias) id为city_id
        put_cache(CITY_PRE, rs)
    return lst


def cities_sys(_city=None):
    sql = city_sql2
    if _city:
        sql = sql + " and (city_name='{}' or alias='{}')".format(_city, _city)
    lst = mysql.query(sql)
    for rs in lst:
        conn.set(CITY_ALIAS_PRE + rs[1], rs[2], ex=CACHE_EX_TIME)
    return lst


def areas(city_id=None, _area=None):
    sql = area_sql
    if _area:
        sql = sql + " and city_id='{}' and (area_name='{}' or alias='{}')".format(city_id, _area, _area)
    lst = mysql.query(sql)
    for rs in lst:
        # rs : (id,area_name,alias,city_id)
        put_cache(AREA_PRE + '{}_'.format(rs[3]), rs[0:3])


def areas_sys(city_id=None, _area=None):
    sql = area_sql2
    if _area:
        sql = sql + " and city_id='{}' and (area_name='{}' or alias='{}')".format(city_id, _area, _area)
    lst = mysql.query(sql)
    for rs in lst:
        conn.set(AREA_ALIAS_PRE + '{}_'.format(rs[3]) + rs[1], rs[2], ex=CACHE_EX_TIME)


def put_cache(pre, dist):
    conn.pipeline() \
        .set(pre + dist[1], '{}:{}'.format(dist[1], dist[0]), ex=CACHE_EX_TIME) \
        .set(pre + dist[2], '{}:{}'.format(dist[1], dist[0]), ex=CACHE_EX_TIME) \
        .execute()


def city(param):
    key = '{}{}'.format(CITY_PRE, param)
    _city = conn.get(key)
    if not _city:
        cities(param)
        _city = conn.get(key)
    return _city


def area(city_id, param):
    key = '{}{}'.format(AREA_PRE + '{}_'.format(city_id), param)
    _area = conn.get(key)
    if not _area:
        areas(city_id, param)
        _area = conn.get(key)
    return _area


def city_alias(param):
    key = '{}{}'.format(CITY_ALIAS_PRE, param)
    _city = conn.get(key)
    if not _city:
        cities_sys(param)
        _city = conn.get(key)
    return _city


def area_alias(city_id, param):
    key = '{}{}'.format(AREA_ALIAS_PRE + '{}_'.format(city_id), param)
    _area = conn.get(key)
    if not _area:
        areas_sys(city_id, param)
        _area = conn.get(key)
    return _area
