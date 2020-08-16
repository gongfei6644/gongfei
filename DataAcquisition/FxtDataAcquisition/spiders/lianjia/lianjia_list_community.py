# -*- coding: utf-8 -*-
# @Time    : 2019-05-23 10:55
# @Author  : luomingming
# @Desc    :

import logging
import re
from copy import copy
from datetime import datetime
from urllib.parse import urljoin

import scrapy

from FxtDataAcquisition.items import ProjectInfoItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.settings import SITE_LIANJIA_COMMUNITY, CRAWL_MAX_PAGE
from FxtDataAcquisition.spiders.common import *

logger = logging.getLogger(__name__)
config_repo = ConfigRepo()
urls = config_repo.get_all_urls(SITE_LIANJIA_COMMUNITY)


class LianjiaListCommunitySpider(scrapy.Spider):
    name = 'lianjia_list_community'
    allowed_domains = ['www.lianjia.com']
    start_urls = urls
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        conf = response.meta.get('conf')
        if not conf:
            conf = config_repo.get_detail(SITE_LIANJIA_COMMUNITY, response.url)
        if conf:
            nodes = response.xpath('//ul[@class="listContent"]/li')

            for node in nodes:
                item = {}
                item['source_link'] = response.url
                item['data_source'] = conf.get('source')
                item['city'] = conf.get('city')
                item['行政区'] = conf.get('area')
                item['片区'] = conf.get('sub_area')
                item = self.parse_list(item, node)
                yield item

            if nodes:
                yield from self.parse_next_page(conf, response)

    def parse_list(self, item, node):
        pn = node.xpath('.//div[@class="title"]/a/text()').extract_first().strip()
        detail_link = node.xpath('.//div[@class="title"]/a/@href').extract_first().strip()
        project_price = node.xpath('.//div[@class="totalPrice"]/span/text()').extract_first().strip()
        case_num = node.xpath('.//div[@class="xiaoquListItemSellCount"]//span/text()').extract_first().strip()
        crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = uuid([detail_link, project_price, crt_time[0:7].replace('-', '')])

        item['_id'] = uid
        item['楼盘名称'] = pn
        item['小区均价'] = project_price
        item['source_link'] = detail_link
        item['crt_time'] = crt_time
        item['在售套数'] = case_num

        return item

    def parse_next_page(self, conf, response):
        next_url = extract(response.xpath("//a[contains(text(),'下一页')]/@href"))
        if next_url and (not next_url.__contains__('javascript')):
            logger.info('{} 获取下一页地址: {}'.format(datetime.now(), next_url))
            yield scrapy.Request(url=next_url, meta={'conf': conf}, callback=self.parse, dont_filter=True)
