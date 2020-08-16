# -*- coding: utf-8 -*-
# @Desc    :

import os
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import zipfile
from datetime import datetime

from flask import jsonify

from app.config import EXPORT_FILE_DIR
from app.dbs.mysql_manager import mysql
from app.service import etl
from app.service.export_std import ExportStdCases
from app.webapi import api

logger = logging.getLogger(__name__)
thread_pool = ThreadPoolExecutor(max_workers=1)


# http://127.0.0.1:5000/api/export/575/南京市/2019-06-20/2019-07-19
@api.route('/export/<int:_id>/<string:city>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
def export(_id, city, start_date, end_date):
    """
    数据导出接口, 非阻塞
    :param _id: mysql主键
    :param city: city_name
    :param start_date:case_happen_date
    :param end_date: case_happen_date
    :return: 接口调用状态
    """
    # t = threading.Thread(target=do_export, args=(_id, city, start_date, end_date,))
    # t.start()
    if '-租金' in city:
        city = city.split('-')[0]
        thread_pool.submit(do_export, _id, city, start_date, end_date)
    else:
        logger.info('city参数错误')
    return jsonify({'code': 0, 'msg': 'ok'})


def do_export(_id, city, start_date, end_date):
    logger.info('ready to export cases... id: {}, city: {}, start: {}, end: {}'
                .format(_id, city, start_date, end_date))
    clean(city, start_date, end_date)
    file_path = export_file(city, start_date, end_date)
    # 将文件路径更新到mysql
    sql = "UPDATE dat_export_acquisitioninfo SET file_path='{}', status=100, mod_time='{}' WHERE id={}" \
        .format(file_path, datetime.now(), _id)
    mysql.update(sql)
    logger.info('{}: [{} - {}]更新mysql数据库'.format(city, start_date, end_date))


# 对数据去重去偏差
def clean(city, start_date, end_date):
    logger.info('ready to clean cases... city: {}, start: {}, end: {}'
                .format(city, start_date, end_date))
    t_start = time.time()
    etl.clean(city, start_date, end_date)
    msg = '{}: [{} - {}]，去重去偏差耗时: [{}]秒'.format(city, start_date, end_date, time.time() - t_start)
    logger.info(msg)


# 导出去重去偏差的标准化案例
def export_file(city, start_date, end_date):
    logger.info('ready to export cases to file... city: {}, start: {}, end: {}'
                .format(city, start_date, end_date))
    t_start = time.time()
    exporter = ExportStdCases(city=city, start_date=start_date, end_date=end_date)
    file_paths = exporter.export()[0]
    msg = '{}: [{} - {}]，案例导出到文件耗时: [{}]秒'.format(city, start_date, end_date, time.time() - t_start)
    logger.info(msg)

    lst = file_paths.split(';')
    ret_path = lst[0]
    if lst.__len__() > 1:
        ret_path = exporter.zip(lst)
    return ret_path.replace(EXPORT_FILE_DIR, '').replace('\\', '\\\\')
