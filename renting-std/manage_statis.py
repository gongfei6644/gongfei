# -*- coding: utf-8 -*-
# @Desc    : 统计：可设置一定间隔不断统计数据

import sys
import time
import traceback
from datetime import datetime

from app import logs, email
from app.service.statistics import *

logs.logger('manage_statis.log')
logger = logging.getLogger(__name__)


def main():
    statis_to_mysql()


if __name__ == '__main__':
    try:
        t_start = time.time()
        main()
        msg = '{} 案例统计耗时: [{}]秒'.format(datetime.now(), time.time() - t_start)
        logger.info(msg)
    except Exception as e:
        msg = '统计程序出现异常: {}'.format(traceback.format_exc())
        logger.error(msg)
        email.send(msg, '统计程序异常')
        # raise e
        sys.exit(1)
    sys.exit(0)
