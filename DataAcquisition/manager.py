import sys
import time
from os import popen
from scrapy.cmdline import execute

from FxtDataAcquisition.settings import ENV

web_list = [
    # "fang",
    # "cityhouse",
    "lianjia"
    # "qfang",
    # "anjuke",
    # "58"
]

def start_city():
    while True:
        popen("scrapy crawl fang_cities_community")
        time.sleep(30*60*60)


def run(spider_name):
    command = ["scrapy", "crawl", spider_name]
    print(command)
    while True:
        execute(command)
        time.sleep(12*60*60)


if __name__ == '__main__':

    if ENV == 'dev':
        spider = "lianjia_cities_community"
    else:
        spider = sys.argv[1].strip('" ')
    print("当前爬虫: {}".format(spider))
    run(spider)









