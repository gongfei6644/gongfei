# -*- coding: utf-8 -*-
# @Desc    : 清理重复、偏差数据

import logging
from datetime import datetime

from pymongo import UpdateOne

from app.models.std_case import StdCase

logger = logging.getLogger(__name__)


def clean(city, start_date, end_date):
    # 将该时间段的数据状态复原
    StdCase().update_status(city, start_date, end_date)  # todo
    logger.info('完成状态复原. city: {}, start: {}, end: {}'
                .format(city, start_date, end_date))

    # 删除重复数据
    StdCase().del_dups(city, start_date, end_date)
    logger.info('完成重复数据删除. city: {}, start: {}, end: {}'
                .format(city, start_date, end_date))

    # # 按用途分类，删除不合格数据
    deal_by_type('usage', '用途类型', city, start_date, end_date, -1)
    logger.info('完成按用途分类，删除不合格数据. city: {}, start: {}, end: {}'
                .format(city, start_date, end_date))

    # 按建筑类型分类，删除不合格数据
    deal_by_type('btype', '建筑类型', city, start_date, end_date, -2)
    logger.info('完成按建筑类型分类，删除不合格数据. city: {}, start: {}, end: {}'
                .format(city, start_date, end_date))
    #
    # # 不考虑别墅类型的，按楼盘分类
    deal_by_type('project', '楼盘类型', city, start_date, end_date, -3, 0.5)
    logger.info('完成不考虑别墅类型的，按楼盘分类，删除不合格数据. city: {}, start: {}, end: {}'
                .format(city, start_date, end_date))


def deal_by_type(d_type, type_desc, city, start_date, end_date, status, percent=0.4):
    lst = StdCase().get_by_type(d_type, city, start_date, end_date)
    up_list = []
    for c in lst:
        avg = (c['t_price'] / c['t_area'])
        if d_type == 'usage':
            print('按用途分类：')
            print(c['_id']['city'],c['_id'].get('project_name'),c['_id'].get('usage'),'总价:',c['t_price'],"总面积:",c['t_area'],"均价:",avg,'ids:',c['ids'])
        elif d_type == 'btype':
            print('按建筑类型分类：')
            print(c['_id']['city'],c['_id'].get('project_name'),c['_id'].get('build_type'),'总价:',c['t_price'],"总面积:",c['t_area'],"均价:",avg,'ids:',c['ids'])
        elif d_type == 'project':
            print('按楼盘分类：')
            print(c['_id']['city'],c['_id'].get('project_name'),'总价:',c['t_price'],"总面积:",c['t_area'],"均价:",avg,'ids:',c['ids'])
        ids = c['ids']
        cases = StdCase().get_by_ids(ids, city)
        for case in cases:
            _id = case.id
            unitprice = float(case.unitprice)
            diff = (unitprice - avg) / avg
            if abs(diff) > percent:
                up_list.append(update_status(_id, status, '案例均价: {}'.format(avg)))
                logger.warn('city: {} id:{}, {}偏差超过{}的案例,单价:{},均价:{},偏差:{}'.format(city, _id, type_desc, percent,unitprice,avg,diff))
            else:
                up_list.append(update_status(_id, 1))
        if len(up_list) > 3000:
            StdCase().bulk_update(up_list, city)
            up_list = []
    if up_list:
        StdCase().bulk_update(up_list, city)

        # for _id in ids:
        #     cs = StdCase().get_by_id(_id, city)
        #     # if d_type == 'project' and str(cs.usage).__contains__('别墅'):
        #     #   continue
        #     diff = (cs.unitprice - avg) / avg
        #     if abs(diff) > percent:
        #         StdCase().update_status_by_id(_id, city, status, '案例均价: {}'.format(avg))
        #         logger.warn('{}偏差超过{}的案例{}'.format(type_desc, percent, _id))
        #     else:
        #         StdCase().update_status_by_id(_id, city, 1)


def update_status(_id, status, remark=None):
    op = UpdateOne({'_id': _id}, {'$set': {
        'status': status, 'std_remark': remark, 'etl_date': datetime.now()
    }}, upsert=False)
    return op


