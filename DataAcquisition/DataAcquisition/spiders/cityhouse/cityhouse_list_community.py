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
from FxtDataAcquisition.settings import SITE_CITYHOUSE_COMMUNITY, CRAWL_MAX_PAGE
from FxtDataAcquisition.spiders.common import *

logger = logging.getLogger(__name__)
config_repo = ConfigRepo()
urls = config_repo.get_all_urls(SITE_CITYHOUSE_COMMUNITY)


class CityhouseListCommunitySpider(scrapy.Spider):
    name = 'cityhouse_list_community'
    allowed_domains = ['www.cityhouse.cn']
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
            conf = config_repo.get_detail(SITE_CITYHOUSE_COMMUNITY, response.url)
        if conf:
            nodes = response.xpath('//div[@class="houselist_singlearea mt20"]')

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
        item['楼盘名称'] = node.xpath('string(.//span[@class="hl_cont_title mr"]/a/text())').extract_first().strip()
        detail_href = node.xpath('string(.//span[@class="hl_cont_title mr"]/a/@href)').extract_first().strip()
        detail_link = urljoin(item["list_page_url"], detail_href)
        price = node.xpath('string(.//span[text()="平均单价"]/following-sibling::span/text())').extract_first().strip()
        unit = node.xpath('.//div[@class="hl_cont_rbox fr tr"]/li/text()').extract()
        project_price = self.make_price(price, unit)
        item['地址'] = node.xpath('.//span[@class="f14 gray3"]/text()').extract_first().strip()
        item['售卖状态'] = node.xpath('string(.//span[@class="hastat"]/text())').extract_first().strip()

        item['建筑年代'] = node.xpath('string(.//font[contains(text(), "建筑年代")]/parent::*/text())').extract_first().strip()
        item["建筑类型"] = node.xpath('string(.//font[contains(text(), "建筑类型")]/parent::*/text())').extract_first().strip()
        item["房屋总数"] = node.xpath('string(.//font[contains(text(), "房屋总数")]/parent::*/text())').extract_first().strip()
        item["楼栋总数"] = node.xpath('string(.//font[contains(text(), "楼栋总数")]/parent::*/text())').extract_first().strip()
        crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = uuid([detail_link, project_price, crt_time[0:7].replace('-', '')])
        item['_id'] = uid
        item['小区均价'] = project_price
        item['source_link'] = detail_link
        item['crt_time'] = crt_time

        return item

    def parse_next_page(self, conf, response):
        next_href = extract(response.xpath("//a[contains(text(),'下一页')]/@href"))
        if next_href and (not next_href.__contains__('javascript')):
            next_url = urljoin(response.url, next_href)
            logger.info('{} 获取下一页地址: {}'.format(datetime.now(), next_url))
            yield scrapy.Request(url=next_url, meta={'conf': conf}, callback=self.parse, dont_filter=True)

    @staticmethod
    def make_price(price, unit):

        if price:
            price = "".join(price).replace(",", "")
            u = "".join(unit)
            if "万" in u:
                return str(int(float(price)*10000))
        return price





