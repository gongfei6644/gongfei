# coding:utf-8
from lxml import etree

from utils.common_downloader_list import crawling
from utils.common_logger import get_logger







def main():
    logger = get_logger("detail", source, logger_path)
    downloader = crawling(source, logger)
    data = downloader.get_by_chrome(url)
    html = etree.HTML(data)


if __name__ == '__main__':
    source = "房天下二手房"
    logger_path = "/usr/local/DataCollection/logs/FxtDataAcquisition/{}".format(source)
    url = "https://sh.esf.fang.com/"
    main()
