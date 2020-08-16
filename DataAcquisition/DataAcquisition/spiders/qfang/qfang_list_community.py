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
from FxtDataAcquisition.spiders.common import *

logger = logging.getLogger(__name__)
config_repo = ConfigRepo()
urls = config_repo.get_all_urls(SITE_QFANG_COMMUNITY)


class QfangListCommunitySpider(scrapy.Spider):
    name = 'qfang_list_community'
    allowed_domains = ['www.qfang.com']
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
            conf = config_repo.get_detail(SITE_QFANG_COMMUNITY, response.url)
        if conf:
            nodes = response.xpath('//div[@class="house-detail"]/ul/li')

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
        pn = node.xpath('string(.//p[@class="house-title"]/a/text())').extract_first().strip()
        detail_href = node.xpath('string(.//p[@class="house-title"]/a/@href)').extract_first().strip()
        project_price = node.xpath('string(.//span[@class="sale-price"]/text())').extract_first().strip()
        if all([pn, detail_href, project_price]):
            detail_link = urljoin(item["list_page_url"], detail_href)
            case_num = node.xpath('.//a[contains(text(), "二手房")]/text()').re(r'\d+')
            item["地址"] = node.xpath(
                'string(.//p[@class="garden-address text clearfix"]/span/text())').extract_first().strip()
            usage = node.xpath('.//p[@class="garden-address clearfix"]/span[last()]/text()').re(r'\S+')
            build_date = node.xpath('.//span[contains(text(), "年建")]/text()').re(r'\d+')
            crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            uid = uuid([detail_link, project_price, crt_time[0:7].replace('-', '')])
            item['uid'] = uid
            item["楼盘名称"] = pn
            item['小区均价'] = project_price
            item['source_link'] = detail_link
            item['crt_time'] = crt_time
            item["用途"] = usage[0] if usage else None
            item["在售套数"] = case_num[0] if case_num else None
            item["建筑年代"] = build_date[0] if build_date else None
            return item

    def parse_next_page(self, conf, response):
        next_url = extract(response.xpath("//a[contains(text(),'下一页')]/@href"))
        if next_url and (not next_url.__contains__('javascript')):
            logger.info('{} 获取下一页地址: {}'.format(datetime.now(), next_url))
            yield scrapy.Request(url=next_url, meta={'conf': conf}, callback=self.parse, dont_filter=True)
