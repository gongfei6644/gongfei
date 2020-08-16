# -*- coding: utf-8 -*-
# @Time    : 2019-01-22 16:35
# @Author  : luomingming


import os
import logging
from logging.handlers import TimedRotatingFileHandler

from FxtDataAcquisition.settings import *


def logger(file, level=LOG_LEVEL, rotating=True):
    """
        file like logs/xxx.log
    """
    log_file = LOG_PATH + file
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    if rotating:
        time_handler = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=15, encoding='utf-8')
        # handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
        time_handler.suffix = "%Y-%m-%d.log"
    else:
        time_handler = logging.FileHandler(log_file, encoding='utf-8')
    time_handler.setLevel(level=level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s - %(message)s',
        '%Y-%m-%d %H:%M:%S')
    time_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=level)

    logging.basicConfig(
        level=level,
        handlers=[console_handler, time_handler]
    )
