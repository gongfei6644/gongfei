# -*- coding: utf-8 -*-
# @Time    : 2019-05-23 10:55
# @Author  : luomingming
# @Desc    :
import base64
import logging
import re
import time
from copy import copy
from datetime import datetime
from urllib.parse import urljoin, quote

import scrapy

from FxtDataAcquisition.items import ProjectInfoItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.spiders.common import *

logger = logging.getLogger(__name__)
config_repo = ConfigRepo()
urls = config_repo.get_all_urls(SITE_FANG_COMMUNITY)


class FangListCommunitySpider(scrapy.Spider):
    name = 'fang_list_community'
    allowed_domains = ['www.fang.com']
    start_urls = urls
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300,
        }
    }

    def start_requests(self):

        for url in urls:
            burl = base64.b64encode(url.encode("utf-8"))
            uurl = quote(burl)
            url += "?_rfss=1"

            referer = "http://search.fang.com/captcha-verify/?t={}&h={}".format("1563157133.231", uurl)
            cookie = "global_cookie=858rxappvbibay2xvvj0knhnj2zjpdnfwnn; Integrateactivity=notincludemc; lastscanpage=0; newhouse_user_guid=8F79FB4C-E7E7-A82F-1EAB-80A740138AA1; budgetLayer=1%7Cbj%7C2019-06-18%2014%3A21%3A27; resourceDetail=1; searchConN=1_1562072520_529%5B%3A%7C%40%7C%3A%5Db2755e4c34cf6f19bdf36bf7f5e7f252; vh_newhouse=1_1562135369_1723%5B%3A%7C%40%7C%3A%5Dc986ba3e7921e9c51a1d863325527852; new_search_uid=6beab057a77eed00b3111dba591ed79b; __utmc=147393320; __utmz=147393320.1562934211.33.19.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/; Captcha=54424F47374E786264774E523870554A6C6367363442334A57532B4A676E6377487836486A496B66726B744E3739722B6D4F456C676A326F7342655A355A7346344B4B77335654306344303D; newhouse_chat_guid=43F0A0FB-EA25-9129-D97D-FC1C6A4025D1; city=sz; __utma=147393320.3500232.1560338584.1563071182.1563153028.35; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.57.10.1563153028; unique_cookie=U_haxkax8249tj5zdl5h0tp1j9l1jjy02o0dx*56"
            headers = {
                "User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
                "referer": referer,
                "cookie": cookie
            }
            yield scrapy.Request(url=url, callback=self.parse, headers=headers, dont_filter=True)

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        conf = response.meta.get('conf')
        if not conf:
            conf = config_repo.get_detail(SITE_FANG_COMMUNITY, response.url)
        if conf:
            nodes = response.xpath('//div[@class="houseList"]//div[contains(@id, "houselist")]')

            for node in nodes:
                item = {}
                item['list_page_url'] = response.url
                item['data_source'] = conf.get('source')
                item['city'] = conf.get('city')
                item['area'] = conf.get('area')
                item['sub_area'] = conf.get('sub_area')
                item = self.parse_list(item, node)
                yield item
            if nodes:
                yield from self.parse_next_page(conf, response)

    def parse_list(self, item, node):
        pn = node.xpath('string(.//a[@class="plotTit"]/text())').extract_first().strip()
        detail_href = node.xpath(
            'string(.//a[@class="plotTit"]/@href)').extract_first().strip()
        project_price = node.xpath('string(.//p[@class="priceAverage"]/span[1]/text())').extract_first().replace(
            'com/esf', 'com/xiangqing')
        if all([pn, detail_href, project_price]):
            detail_link = "https:" + detail_href if detail_href.startswith("//") else urljoin(
                item["list_page_url"], detail_href)
            item["用途"] = node.xpath('string(.//span[@class="plotFangType"]/text())').extract_first().strip()
            case_num = node.xpath('string(.//li[contains(text(), "套在售")]/a/text())').re(r'\d+')

            crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            uid = uuid([detail_link, project_price, crt_time[0:7].replace('-', '')])
            item['_id'] = uid
            item['楼盘名称'] = pn
            item['小区均价'] = project_price
            item['source_link'] = detail_link
            item['crt_time'] = crt_time
            item["在售套数"] = case_num[0] if case_num else None
            return item


    def parse_next_page(self, conf, response):
        next_url = extract(response.xpath("//a[contains(text(),'下一页')]/@href"))
        if next_url and (not next_url.__contains__('javascript')):
            logger.info('{} 获取下一页地址: {}'.format(datetime.now(), next_url))
            yield scrapy.Request(url=next_url, meta={'conf': conf}, callback=self.parse, dont_filter=True)
