# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from copy import copy
from datetime import datetime
from FxtDataAcquisition.items import CaseItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.utils.functions import *
from FxtDataAcquisition.spiders.common import *
from FxtDataAcquisition.settings import SITE_FANGTAN, CRAWL_MAX_PAGE

logger = logging.getLogger(__name__)
config_repo = ConfigRepo()
urls = config_repo.get_all_urls(SITE_FANGTAN)


class FangtanListSpider(scrapy.Spider):
    name = 'fangtan_list'
    allowed_domains = ['www.fangtan007.com']
    start_urls = urls
    custom_settings = {
        # 'CONCURRENT_REQUESTS': 16,
        # 'LOG_LEVEL': "DEBUG",
        # 'LOG_FILE': LOG_PATH + "fangtan_list.log",
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
            conf = config_repo.get_detail(SITE_FANGTAN, response.url)
        if conf:
            is_last_month = False
            nodes = response.css('.fang-list li')
            for node in nodes:
                date_interval = extract(node.xpath(".//div[@class='jiage']/div[3]/span/text()"))
                r = compute_case_date(date_interval)
                is_last_month = r[0]
                case_happen_date = r[1]
                if is_last_month:
                    break
                if not case_happen_date:
                    continue
                item = CaseItem()
                item['list_page_url'] = response.url
                item['case_happen_date'] = case_happen_date
                item['data_source'] = conf.get('source')
                item['city'] = conf.get('city')
                item['area'] = conf.get('area')
                item['sub_area'] = conf.get('sub_area')
                item = self.parse_list(item, node)
                # 字段统计
                statis_list(item)
                yield item
            if nodes and not is_last_month:
                yield from self.parse_next_page(conf, response)

    def parse_list(self, item, node):
        item['title'] = extract(node.css('.title a::text'))
        detail_link = extract(node.css('.title a::attr(href)'))
        source_link = re.sub('/sale/.+', detail_link, item['list_page_url'])
        unit_price = extract(node.xpath(".//div[@class='jiage']/div[2]/text()"))
        unit_price = re.match('\d+', unit_price).group()
        crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = uuid([source_link, unit_price, crt_time[0:7].replace('-', '')])
        item['_id'] = uid
        item['unitprice'] = unit_price
        item['source_link'] = source_link
        item['crt_time'] = crt_time
        item['project_name'] = extract(node.xpath(".//div[@class='adds']/a[1]/text()"))
        tmp = extract(node.xpath(".//div[@class='qita']/span[1]/text()"))
        item['house_area'] = re.match('\d+', tmp).group()
        return item

    def parse_next_page(self, conf, response):
        next_url = response.xpath("//div[@class='page']/a[contains(text(),'下一页')]/@href").extract_first()
        if next_url and (not next_url.__contains__('javascript')):
            page_num = 0
            page_node = extract(response.xpath("//div[@class='page']/a[@class='ol']/text()"))
            if page_node:
                page_num = int(page_node)
            if page_num <= CRAWL_MAX_PAGE:
                next_url = re.sub('/sale/.+', next_url, response.url)
                logger.info('{} 获取下一页地址: {}'.format(datetime.now(), next_url))
                yield scrapy.Request(url=next_url, meta={'conf': conf}, callback=self.parse, dont_filter=True)
