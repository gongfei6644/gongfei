import os
import time
import logging


def get_logger(city, source, logger_path):
    logger_path = os.path.join(logger_path, source)
    if not os.path.exists(logger_path):
        os.makedirs(logger_path)
    log_time = time.strftime("_%Y-%m-%d.log", time.localtime())
    log_name = logger_path + city + log_time
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

    return logger

