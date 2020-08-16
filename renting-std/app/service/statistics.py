# -*- coding: utf-8 -*-
# @Desc    : 统计服务

import logging

from app.dbs.mysql_manager import mysql
from app.models.case import Case
from app.service.sqls.case_statis_sql import *

logger = logging.getLogger(__name__)


def statis_to_mysql():
    # 统计案例
    update_or_insert(Case().statis('case_count'), 'case_count')

    # 统计有楼盘名的量
    update_or_insert(Case().statis('proj_name_count'), 'proj_name_count')

    # 统计有建筑面积的量
    update_or_insert(Case().statis('buildarea_count'), 'buildarea_count')

    # 统计有单价的量
    update_or_insert(Case().statis('unitprice_count'), 'unitprice_count')

    # 统计标准化量
    update_or_insert(Case().statis_std(), 'std_count')


def update_or_insert(cases, s_type):
    for case in cases:
        city = case['_id']['city']
        if not str(city).__contains__('市'):
            city = city + '市'
        source = case['_id']['data_source']
        a_time = case['_id']['time']
        st = get_statis(city, source, a_time)
        count = case['count']
        if not st:
            insert_statis(count, city, source, a_time, s_type)
        else:
            if s_type == 'case_count':
                st[0]['case_count'] = count
            elif s_type == 'proj_name_count':
                st[0]['projectname_count'] = count
            elif s_type == 'buildarea_count':
                st[0]['buildarea_count'] = count
            elif s_type == 'unitprice_count':
                st[0]['unitprice_count'] = count
            elif s_type == 'std_count':
                st[0]['standardized_count'] = count
            update_statis(st[0])


def get_statis(city, source, a_time):
    s = mysql.query_(select_statis_sql.format(city, source, a_time))
    return s


def update_statis(statis):
    cc = statis['case_count'] if statis['case_count'] else 'null'
    pc = statis['projectname_count'] if statis['projectname_count'] else 'null'
    bc = statis['buildarea_count'] if statis['buildarea_count'] else 'null'
    uc = statis['unitprice_count'] if statis['unitprice_count'] else 'null'
    sc = statis['standardized_count'] if statis['standardized_count'] else 'null'
    sql = update_statis_sql.format(cc, pc, bc, uc, sc, statis['id'])
    rs = mysql.update(sql)
    logger.info('案例统计sql: {}, 更新结果: {}'.format(sql, rs))


def insert_statis(count, city, source, a_time, s_type):
    cc = 'null'
    pc = 'null'
    bc = 'null'
    uc = 'null'
    sc = 'null'
    if s_type == 'case_count':
        cc = count
    elif s_type == 'proj_name_count':
        pc = count
    elif s_type == 'buildarea_count':
        bc = count
    elif s_type == 'unitprice_count':
        uc = count
    elif s_type == 'std_count':
        sc = count

    sql = insert_statis_sql.format(city, source, cc, pc, bc, uc, sc, a_time)
    # print(sql)
    rs = mysql.update(sql)
    logger.info('案例统计sql: {}, 新增结果: {}'.format(sql, rs))
