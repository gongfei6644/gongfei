# -*- coding: utf-8 -*-
# @Time    : 2019-05-23 10:55
# @Author  : luomingming
# @Desc    :

import copy
import re

import scrapy

from FxtDataAcquisition.spiders.common import *
from FxtDataAcquisition.items import CityItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.service import distinct
from FxtDataAcquisition.settings import SITE_ANJUKE_COMMUNITY

config_repo = ConfigRepo()


class AnjukeCitiesCommunitySpider(scrapy.Spider):
    name = 'anjuke_cities_community'
    allowed_domains = ['www.anjuke.com']
    start_urls = ['https://www.anjuke.com/sy-city.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CityPipeline': 300,
        }
    }

    def parse(self, response):
        nodes = response.css('.city_list a')
        for node in nodes:
            city = extract(node.css('::text'))
            source = SITE_ANJUKE_COMMUNITY
            city = get_full_city_name(city)
            # # 先删除原始数据
            # config_repo.delete(source, city)

            item = CityItem()
            url = extract(node.css('::attr(href)'))
            item['city'] = city
            item['source'] = source
            yield scrapy.Request(url=url + '/community/?from=navigation', meta={'item': item},
                                 callback=self.parse_area, dont_filter=True)

    def parse_area(self, response):
        im = response.meta['item']
        city = extract(response.css('.cityselect div:nth-child(1)::text'))
        city_f = get_full_city_name(city)
        nodes = response.css('.items-list div:nth-child(1) .elems-l a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = extract(node.css('::text'))
            if name == '全部':
                continue
            if city_f:
                item['city'] = city_f
            item['area'] = name
            url = extract(node.css('::attr(href)'))
            yield scrapy.Request(url=url, meta={'item': item},
                                 callback=self.parse_sub_area, dont_filter=True)

    def parse_sub_area(self, response):
        im = response.meta['item']
        nodes = response.css('.elems-l .sub-items a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = extract(node.css('::text'))
            if name == '全部':
                continue
            if not config_repo.exist(item['source'], name):
                item['sub_area'] = name
                item['sub_area_url'] = extract(node.css('::attr(href)'))
                yield item
