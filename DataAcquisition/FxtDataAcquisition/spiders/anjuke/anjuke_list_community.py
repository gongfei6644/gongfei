# -*- coding: utf-8 -*-
# @Time    : 2019-05-23 10:55
# @Author  : luomingming
# @Desc    :

import logging
import re
from copy import copy
from datetime import datetime

import scrapy

from FxtDataAcquisition.items import ProjectInfoItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.settings import SITE_ANJUKE_COMMUNITY, CRAWL_MAX_PAGE
from FxtDataAcquisition.spiders.common import *

logger = logging.getLogger(__name__)
config_repo = ConfigRepo()
urls = config_repo.get_all_urls(SITE_ANJUKE_COMMUNITY)


class AnjukeListCommunitySpider(scrapy.Spider):
    name = 'anjuke_list_community'
    allowed_domains = ['www.anjuke.com']
    start_urls = urls
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        conf = None
        if 'conf' in response.meta.keys():
            meta = copy(response.meta)
            conf = meta['conf']
        if not conf:
            conf = config_repo.get_detail(SITE_ANJUKE_COMMUNITY, response.url)
        if conf:
            nodes = response.css('.list-content div[_soj=xqlb]')
            for node in nodes:
                item = {}
                item['list_page_url'] = response.url
                item['data_source'] = conf.get('source')
                item['city'] = conf.get('city')
                item['行政区'] = conf.get('area')
                item['片区'] = conf.get('sub_area')
                item = self.parse_list(item, node)
                yield item
            if nodes:
                yield from self.parse_next_page(conf, response)

    def parse_list(self, item, node):
        pn = node.css('.li-info h3 a')
        project_name = extract(pn.css('::text'))
        detail_link = extract(pn.css('::attr(href)'))
        project_price = node.xpath('string(.//div[@class="li-side"]//strong/text())').extract_first().strip()
        build_date = node.css('.li-info .date::text').re(r'\d+')
        crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = uuid([detail_link, project_price, crt_time[0:7].replace('-', '')])
        item['_id'] = uid
        item['crt_time'] = crt_time
        item['source_link'] = detail_link
        item['build_date'] = build_date[0] if build_date else None
        item['小区均价'] = project_price
        item['楼盘名称'] = project_name
        item['地址'] = extract(node.css(".li-info address::text"))
        return item

    def parse_next_page(self, conf, response):
        next_url = extract(response.xpath(
            "//div[@class='page-content']/div[@class='multi-page']/a[contains(text(),'下一页')]/@href"))
        if next_url and (not next_url.__contains__('javascript')):
            logger.info('{} 获取下一页地址: {}'.format(datetime.now(), next_url))
            yield scrapy.Request(url=next_url, meta={'conf': conf}, callback=self.parse, dont_filter=True)

