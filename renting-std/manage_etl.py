# -*- coding: utf-8 -*-
# @Desc    : 2.清理重复、偏差数据：月初清理上月数据，不可时刻运行

import sys
import time
import traceback

from app import logs, email
from app.service.etl import *

logs.logger('manage_etl.log')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        start_date = sys.argv[2]
        end_date = sys.argv[3]

        t_start = time.time()
        clean(sys.argv[1], start_date, end_date)
        msg = '[{} - {}]时间段的案例去重去偏差耗时: [{}]秒'.format(start_date, end_date, time.time() - t_start)
        logger.info(msg)

        # 去重去偏差之后，执行自动入库
        # t_start = time.time()
        # auto_in()
        # msg = '{} 案例入库耗时: [{}]秒'.format(datetime.now(), time.time() - t_start)
        # logger.info(msg)
    except Exception as e:
        msg = '数据清洗程序出现异常: {}'.format(traceback.format_exc())
        logger.error(msg)
        email.send(msg, '案例清洗程序异常')
        # raise e
        sys.exit(1)
    sys.exit(0)
