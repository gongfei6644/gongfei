# -*- coding: utf-8 -*-
# @Desc    : 3.自动入库: 月初执行上月数据的入库
# 注：此启动类在生产环境不执行，入库已经放到manage_etl.py中执行。
# 因为自动入库必需等待etl处理完才能进行。

import sys
import time

from app import email
from app import logs
from app.config import IS_AUTO_FDC
from app.service.storage import *
from app.service.export_std import ExportStdCases

logs.logger('manage_storage.log')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        start_date = sys.argv[2]
        end_date = sys.argv[3]

        t_start = time.time()
        exporter = ExportStdCases(city=sys.argv[1], start_date=start_date, end_date=end_date)
        file_paths = exporter.export()[0]
        if IS_AUTO_FDC:
            upload(file_paths)
        msg = '[{} - {}]时间段的案例入库耗时: [{}]秒'.format(start_date, end_date, time.time() - t_start)
        logger.info(msg)
    except Exception as e:
        msg = '自动入库程序出现异常: {}'.format(traceback.format_exc())
        logger.error(msg)
        email.send(msg, '案例自动入库程序异常')
        # raise e
        sys.exit(1)
    sys.exit(0)
