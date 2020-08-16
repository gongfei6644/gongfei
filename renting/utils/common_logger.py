import os
import re
import time
import logging
import datetime as dt
import traceback
from utils.constants import LOG_EXPIRED


def get_logger(city, source, log_path):
    log_path = os.path.join(log_path, source) + "/"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    try:
        files = os.listdir(log_path)
        cur_dt = dt.datetime.now()
        for file in files:
            dt_str = re.findall(r'_\d{4}-\d{2}-\d{2}.log', file)
            if dt_str:
                log_dt = dt.datetime.strptime(dt_str[0], "_%Y-%m-%d.log")
                delta_dt = cur_dt - log_dt
                if delta_dt.days > LOG_EXPIRED:
                    file_path = os.path.join(log_path, file)
                    os.remove(file_path)
    except Exception as e:
        print(e)
        print(traceback.print_exc())
    try:
        log_time = time.strftime("_%Y-%m-%d.log", time.localtime())
        log_name = log_path + city + log_time
        print("log_name", log_name)
        logger = logging.getLogger(log_name)
        logger.setLevel(level=logging.DEBUG)
        handler = logging.FileHandler(log_name, encoding='utf-8')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)

        logger.addHandler(handler)
        logger.addHandler(console)
    except Exception as e:
        print(e)
        print(traceback.print_exc())
    else:
        return logger

