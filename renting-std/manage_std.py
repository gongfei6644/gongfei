# -*- coding: utf-8 -*-
# @Desc    : 1.标准化：可时刻运行

import logging
import os
import sys
import traceback

from app import logs, email
from app.service import std
from app.service.distinct import *

log_file = 'manage_std_{}.log'.format(os.getpid())
if len(sys.argv) > 1:
    log_file = sys.argv[1]
logs.logger(log_file)
logger = logging.getLogger(__name__)


def init():
    # 初始化行政区信息
    print('执行标准化初始化....')
    cities()
    areas()
    cities_sys()
    areas_sys()
    print('初始化完成....')


def main():
    init()
    # dbs = conn.list_database_names()
    # dbs = conn['DataCollecting']
    # collection = dbs['Dat_case']
    # list = collection.find()
    # for data in list:
    #   std.std(data)

    std.std()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        msg = '标准化程序出现异常: {}'.format(traceback.format_exc())
        logger.error(msg)
        email.send(msg, '标准化程序异常')
        # raise e
        sys.exit(1)
    sys.exit(0)
