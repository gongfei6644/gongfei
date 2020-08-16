# -*- coding: utf-8 -*-
# @Time    : 2019-05-07 20:32
# @Author  : luomingming
# @Desc    :

import logging
import traceback

from apscheduler.schedulers.blocking import BlockingScheduler
from bson import json_util
from pymongo import UpdateOne, InsertOne

from FxtDataAcquisition.repository.case_repo import CaseRepo
from FxtDataAcquisition.repository.project_info_repo import ProjectInfoRepo
from FxtDataAcquisition.utils import logs, email
from FxtDataAcquisition.utils.redis_client import rediz

logs.logger('schedule_persist_cases.log')
logger = logging.getLogger(__name__)
case_repo = CaseRepo()
pinfo_repo = ProjectInfoRepo()


def persist_list():
    persist('insert_list')


def persist_detail():
    persist('update_detail')


def persist_list_community():
    persist_community('insert_list_community')


def persist_detail_community():
    persist_community('update_detail_community')


def persist(key):
    repo = case_repo
    try:
        lst = rediz.smembers(key)
        if lst:
            mp = {}
            for cs in lst:
                case = json_util.loads(cs, encoding='utf-8')
                ck = case['city']
                if key.__contains__('insert_list'):
                    op = InsertOne(case)
                else:
                    op = UpdateOne({'_id': case['_id']}, {'$set': case}, upsert=False)
                if ck not in mp:
                    mp[ck] = [op]
                else:
                    tmp = mp[ck]
                    tmp.append(op)
            for k in mp.keys():
                logger.info('持久化{}的数据'.format(k))
                vs = mp[k]
                ret = repo.batch_update(k, vs)
            rediz.srem(key, *lst)
    except Exception as e:
        email.send(key + ', 异常: {}'.format(traceback.format_exc()), '案例持久化异常(重要!!!)')


def persist_community(key):
    repo = pinfo_repo
    batch_list = []
    try:
        lst = rediz.smembers(key)
        for cs in lst:
            case = json_util.loads(cs, encoding='utf-8')
            if key.__contains__('insert_list'):
                op = InsertOne(case)
            else:
                op = UpdateOne({'_id': case['_id']}, {'$set': case}, upsert=False)
            batch_list.append(op)
        if batch_list:
            print("{} {}条".format(key, len(batch_list)))
            ret = repo.batch_update(batch_list)
            rediz.srem(key, *lst)
    except Exception as e:
        email.send(key + ', 异常: {}'.format(traceback.format_exc()), '案例持久化异常(重要!!!)')


def start():
    logger.info('持久化调度任务启动成功.')
    scheduler = BlockingScheduler()
    # 二手房案例持久化
    scheduler.add_job(func=persist_list, trigger='cron', second='*/6')
    scheduler.add_job(func=persist_detail, trigger='cron', second='*/6')

    # 小区信息持久化
    scheduler.add_job(func=persist_list_community, trigger='cron', second='*/6')
    scheduler.add_job(func=persist_detail_community, trigger='cron', second='*/6')
    scheduler.start()


if __name__ == '__main__':
    start()
