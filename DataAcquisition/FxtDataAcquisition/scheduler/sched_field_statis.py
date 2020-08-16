# -*- coding: utf-8 -*-
# @Time    : 2019-04-19 11:01
# @Author  : luomingming
# @Desc    :


import json
import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from FxtDataAcquisition.settings import *
from FxtDataAcquisition.utils import logs, email
from FxtDataAcquisition.utils.mq_client import mq
from FxtDataAcquisition.utils.redis_client import rediz

logs.logger('sched_field_statis.log')
logger = logging.getLogger(__name__)


def send_msg(name, message_type, collect_type):
    try:
        msg = ''
        statis = rediz.hgetall(name)
        dt = get_statis(statis)
        for s in dt:
            v = dt[s]
            sp = s.split("@")
            crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            case_count = None
            pn_count = None
            up_count = None
            ha_count = None
            if 'case_count' in v.keys():
                case_count = v['case_count']
            if 'project_name' in v.keys():
                pn_count = v['project_name']
            if 'unitprice' in v.keys():
                up_count = v['unitprice']
            if 'house_area' in v.keys():
                ha_count = v['house_area']
            msg = json.dumps(
                {"messagetype": message_type, 'collecttype': collect_type,
                 "website": sp[0], "cityname": sp[1], "crt_time": crt_time,
                 "case_count": case_count,
                 "projectname_count": pn_count,
                 "unitprice_count": up_count,
                 "buildarea_count": ha_count
                 }
            )
            logger.info('{} ready to send msg: '.format(msg))
            mq.send_msg(queue='daq-state-report-queue',
                        exchange='daq-info', routing_key='state-report',
                        msg=msg)
            if message_type == 'increase':
                delete_incr(name, statis)
    except Exception as e:
        email.send(msg + ', 异常: {}'.format(e), '统计信息发送异常')
    if not dt:
        logger.info('{} no msg to send, message type: {}, collect type: {}.'
                    .format(datetime.now(), message_type, collect_type))


def delete_incr(name, statis):
    for s in statis:
        ret = rediz.hdel(name, s)


def get_statis(statis):
    dt = dict()
    for s in statis:
        v = statis[s]
        sp = s.split("-")
        if sp[0] in dt.keys():
            dt[sp[0]].update({sp[1]: v})
        else:
            dt[sp[0]] = {sp[1]: v}
    return dt


def send_incr_list():
    send_msg(STATIS_LIST_INCR_KEY, 'increase', 'list')


def send_incr_detail():
    send_msg(STATIS_DETAIL_INCR_KEY, 'increase', 'details')


def send_list():
    send_msg(STATIS_LIST_KEY, 'total', 'list')


def send_detail():
    send_msg(STATIS_DETAIL_KEY, 'total', 'details')


# 零点清理total统计量
def clear_total_statis():
    logger.info('准备清除total统计量...')
    for name in [STATIS_LIST_KEY, STATIS_DETAIL_KEY]:
        statis = rediz.hgetall(name)
        if statis:
            delete_incr(name, statis)
    logger.info('total统计量清理完毕!')


def start():
    logger.info('字段统计调度任务启动成功.')
    scheduler = BlockingScheduler()
    # scheduler.add_job(my_job, 'cron', year=2017, month=3, day=22, hour=17, minute=19, second=7)
    scheduler.add_job(func=send_incr_list, trigger='cron', hour='*/1')
    scheduler.add_job(func=send_incr_detail, trigger='cron', hour='*/1')
    scheduler.add_job(func=send_list, trigger='cron', hour='*/1')
    scheduler.add_job(func=send_detail, trigger='cron', hour='*/1')

    scheduler.add_job(func=clear_total_statis, trigger='cron', hour=0, minute=0, second=0)
    scheduler.start()


if __name__ == '__main__':
    start()
