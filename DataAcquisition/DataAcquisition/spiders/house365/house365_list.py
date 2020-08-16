# -*- coding: utf-8 -*-
# @Time    : 2019-04-29 10:05
# @Author  : luomingming
# @Desc    :

import logging
import re
from copy import copy
from datetime import datetime

import scrapy

from FxtDataAcquisition.items import CaseItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.settings import SITE_HOUSE365, CRAWL_MAX_PAGE
from FxtDataAcquisition.spiders.common import *
from FxtDataAcquisition.utils.functions import *

logger = logging.getLogger(__name__)
config_repo = ConfigRepo()
urls = config_repo.get_all_urls(SITE_HOUSE365)


class House365ListSpider(scrapy.Spider):
    name = 'house365_list'
    allowed_domains = ['www.house365.com']
    start_urls = urls
    custom_settings = {
        # 'CONCURRENT_REQUESTS': 16,
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CasePipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        conf = None
        if 'conf' in response.meta.keys():
            meta = copy(response.meta)
            conf = meta['conf']
        if not conf:
            conf = config_repo.get_detail(SITE_HOUSE365, response.url)
        if conf:
            nodes = response.css('.infolist_cont .info_list dl')
            if not nodes:
                nodes = response.css('.listPagBox .list .listItem')
            for node in nodes:
                item = CaseItem()
                item['list_page_url'] = response.url
                item['data_source'] = conf.get('source')
                item['city'] = conf.get('city')
                item['area'] = conf.get('area')
                item['sub_area'] = conf.get('sub_area')
                self.parse_list(item, node)

                statis_list(item)
                yield item

            if nodes:
                yield from self.parse_next_page(conf, response)

    def parse_list(self, item, node):
        t_n = node.xpath("./dd[1]/a")
        if not t_n:
            t_n = node.xpath("./div[@class='info']/h3/a")
        if t_n:
            item['title'] = extract(t_n.xpath("text()"))
        detail_link = t_n.xpath("@href").extract_first()
        unit_price = extract(node.xpath("./dd[2]/span[1]/text()"))
        if not unit_price:
            unit_price = extract(node.xpath("./div[@class='unitPrice']/span/text()"))
        if unit_price:
            unit_price = re.match('\d+', unit_price).group()
        crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = uuid([detail_link, unit_price, crt_time[0:7].replace('-', '')])
        item['_id'] = uid
        item['unitprice'] = unit_price
        item['source_link'] = detail_link
        item['crt_time'] = crt_time
        project_name = node.xpath("./dd[2]/a[1]/text()")
        if not project_name:
            project_name = node.xpath("./dd[2]/text()")
        if not project_name:
            project_name = node.xpath("./div[@class='info']/div[2]/a[1]/text()")
            if not project_name:
                project_name = node.xpath("./div[@class='info']/div[2]/font/text()")
            if not project_name:
                project_name = node.xpath("./div[@class='info']/div[2]/text()")
            if not project_name:
                project_name = node.xpath("./div[@class='info']/div[1]/a[1]/text()")
            if not project_name:
                project_name = node.xpath("./div[@class='info']/div[1]/font/text()")
        if project_name:
            item['project_name'] = extract(project_name)
        tmp = node.xpath("./dd[3]/span/text()").extract()
        house_area = None
        for v in tmp:
            if v.__contains__('m&sup2'):
                house_area = v
                break
        if not house_area:
            house_area = extract(node.xpath("./div[@class='acreage']/text()"))
        if house_area:
            item['house_area'] = re.match('\d+', house_area.strip()).group()

    def parse_next_page(self, conf, response):
        next_url = response.xpath("//div[@id='pagebtngroup']/p/a[contains(text(),'下一页')]/@href").extract_first()
        if not next_url:
            next_url = response.xpath("//div/ul[@class='pageList']/li/a[contains(text(),'下一页')]/@href").extract_first()
        if next_url and (not next_url.__contains__('javascript')):
            page_num = 0
            page_node = extract(response.xpath("//div[@id='pagebtngroup']/p/a[@class='btn on']/text()"))
            if not page_node:
                page_node = extract(response.xpath(
                    "//div/ul[@class='pageList']/li/a[@class='btn_num pageon']/text()"))
            if page_node:
                page_num = int(page_node)
            if page_num <= CRAWL_MAX_PAGE:
                logger.info('{} 获取下一页地址: {}'.format(datetime.now(), next_url))
                yield scrapy.Request(url=next_url, meta={'conf': conf}, callback=self.parse, dont_filter=True)
