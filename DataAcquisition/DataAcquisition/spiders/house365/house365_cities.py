# -*- coding: utf-8 -*-
import scrapy
import copy
from FxtDataAcquisition.items import CityItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.settings import SITE_HOUSE365
from FxtDataAcquisition.service import distinct
from FxtDataAcquisition.spiders.common import *

config_repo = ConfigRepo()


class House365CitiesSpider(scrapy.Spider):
    name = 'house365_cities'
    allowed_domains = ['www.house365.com']
    start_urls = ['http://nj.house365.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CityPipeline': 300,
        }
    }

    def parse(self, response):
        nodes = response.css('.sm_station * a')
        for node in nodes:
            city = extract(node.css('::text'))
            source = SITE_HOUSE365
            city = get_full_city_name(city)
            # # 先删除原始数据
            # config_repo.delete(source, city)

            item = CityItem()
            url = node.css('::attr(href)').extract_first()
            item['city'] = city
            item['source'] = source
            suffix = '.sell.house365.com/district/'
            pre = url[0:url.index('.')]
            yield scrapy.Request(url=pre + suffix, meta={'item': item},
                                 callback=self.parse_area, dont_filter=True)

    def parse_area(self, response):
        im = response.meta['item']
        nodes = response.css('#qushu dd a')
        if not nodes:
            nodes = response.css('.itemBox dd a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = extract(node.css('::text'))
            if name == '全部' or name == '任意':
                continue
            item['area'] = name
            url = node.css('::attr(href)').extract_first()
            yield scrapy.Request(url=url, meta={'item': item},
                                 callback=self.parse_sub_area, dont_filter=True)

    def parse_sub_area(self, response):
        im = response.meta['item']
        nodes = response.css('#qushu_g d1 dd a')
        if not nodes:
            nodes = response.css('.areaTypeInner dd a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = extract(node.css('::text'))
            if name == '全部' or name == '任意':
                continue
            if not config_repo.exist(item['source'], name):
                item['sub_area'] = name
                url = node.css('::attr(href)').extract_first()
                item['sub_area_url'] = url
                yield item
