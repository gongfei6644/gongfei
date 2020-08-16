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


class QfangCitiesCommunitySpider(scrapy.Spider):
    name = 'qfang_cities_community'
    allowed_domains = ['www.qfang.com']
    start_urls = ['https://shenzhen.qfang.com/garden']
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CityPipeline': 300,
        }
    }

    def parse(self, response):
        nodes = response.xpath('//ul[@class="cities-opts clearfix"]/li[@class="clearfix"]/p/a')
        for node in nodes:
            item = CityItem()
            city = node.xpath('string(./text())').extract_first().strip()
            source = SITE_QFANG_COMMUNITY
            city = get_full_city_name(city)
            # # 先删除原始数据
            # config_repo.delete(source, city)

            href = node.xpath('string(./@href)').extract_first().strip()
            if href.endswith("/sale"):
                url = "https:" + href.replace("/sale", "/garden")
                item['city'] = city
                item['source'] = source
                yield scrapy.Request(
                    url=url, meta={'item': item}, callback=self.parse_area, dont_filter=True)


    def parse_area(self, response):
        print([response.status, response.url])
        im = response.meta['item']
        nodes = response.xpath('//ul[@class="search-area-detail clearfix"]//a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = node.xpath('string(./text())').extract_first().strip()
            if not any(["周边" in name, "旅游" in name, "风景" in name,
                "名胜" in name, "其他" in name, "其它" in name, "不限" in name, "周边" in name]):
                item['area'] = name
                href = node.xpath('string(./@href)').extract_first().strip()
                url = urljoin(response.url, href)

                yield scrapy.Request(url=url, meta={'item': item},
                    callback=self.parse_sub_area, dont_filter=True)

    def parse_sub_area(self, response):
        im = response.meta['item']
        nodes = response.xpath('//ul[@class="search-area-second clearfix"]//a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = node.xpath('string(./text())').extract_first().strip()
            if not any(["周边" in name, "旅游" in name, "风景" in name,
                        "名胜" in name, "其他" in name, "其它" in name, "不限" in name, "周边" in name]):
                if not config_repo.exist(item['source'], name):
                    href = node.xpath('string(./@href)').extract_first().strip()
                    item['sub_area'] = name
                    item['sub_area_url'] = urljoin(response.url, href)
                    yield item
