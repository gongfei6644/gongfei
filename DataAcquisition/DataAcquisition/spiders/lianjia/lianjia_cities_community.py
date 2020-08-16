# -*- coding: utf-8 -*-
# @Time    : 2019-05-23 10:55
# @Author  : luomingming
# @Desc    :

import copy
import re
from urllib.parse import urljoin

import scrapy

from FxtDataAcquisition.spiders.common import *
from FxtDataAcquisition.items import CityItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.service import distinct
from FxtDataAcquisition.settings import SITE_LIANJIA_COMMUNITY

config_repo = ConfigRepo()


class LianjiaCitiesCommunitySpider(scrapy.Spider):
    name = 'lianjia_cities_community'
    allowed_domains = ['www.lianjia.com']
    start_urls = ['https://www.lianjia.com/city/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CityPipeline': 300,
        },
        'LOG_PATH': '/usr/local/DataCollection/logs/FxtDataAcquisition/{}/'.format(name)
    }

    def parse(self, response):
        nodes = response.xpath('//div[@class="city_province"]/ul/li')
        for node in nodes:
            item = CityItem()
            city = node.xpath('./a/text()').extract_first().strip()
            source = SITE_LIANJIA_COMMUNITY
            city = get_full_city_name(city)
            # # 先删除原始数据
            # config_repo.delete(source, city)

            url = node.xpath('./a/@href').extract_first().strip()
            item['city'] = city
            item['source'] = source
            yield scrapy.Request(url=url + 'xiaoqu/', meta={'item': item},
                                 callback=self.parse_area, dont_filter=True)

    def parse_area(self, response):
        im = response.meta['item']
        nodes = response.xpath('//div[@data-role="ershoufang"]/div[1]/a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = node.xpath('./text()').extract_first().strip()
            item['area'] = name
            href = node.xpath('./@href').extract_first().strip()
            url = urljoin(response.url, href)
            yield scrapy.Request(url=url, meta={'item': item},
                                 callback=self.parse_sub_area, dont_filter=True)

    def parse_sub_area(self, response):
        im = response.meta['item']
        nodes = response.xpath('//div[@data-role="ershoufang"]/div[2]/a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = node.xpath('./text()').extract_first().strip()
            if not config_repo.exist(item['source'], name):
                href = node.xpath('./@href').extract_first().strip()
                item['sub_area'] = name
                item['sub_area_url'] = urljoin(response.url, href)

                yield item
