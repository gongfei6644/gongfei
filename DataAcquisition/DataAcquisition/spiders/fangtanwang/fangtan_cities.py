# -*- coding: utf-8 -*-
import scrapy
import re
import copy
from FxtDataAcquisition.items import CityItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.settings import SITE_FANGTAN
from FxtDataAcquisition.service import distinct
from FxtDataAcquisition.spiders.common import *

config_repo = ConfigRepo()


class FangtanCitiesSpider(scrapy.Spider):
    name = 'fangtan_cities'
    allowed_domains = ['www.fangtan007.com']
    start_urls = ['http://www.fangtan007.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CityPipeline': 300,
        }
    }

    def parse(self, response):
        nodes = response.css('.city-name a')
        for node in nodes:
            city = extract(node.css('::text'))
            source = SITE_FANGTAN
            city = get_full_city_name(city)
            # # 先删除原始数据
            # config_repo.delete(source, city)

            item = CityItem()
            #url = node.xpath('@href').extract_first()
            url = node.css('::attr(href)').extract_first()
            item['city'] = city
            item['source'] = source
            # print('-----------------{}'.format(id(item)))
            yield scrapy.Request(url=url + '/sale', meta={'item': item},
                                 callback=self.parse_area, dont_filter=True)

    def parse_area(self, response):
        im = response.meta['item']
        # print('=================={}'.format(id(im)))
        nodes = response.css('.quyun-box-t dd a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = extract(node.css('::text'))
            if name == '不限':
                continue
            item['area'] = name
            url = node.css('::attr(href)').extract_first()
            url = response.url.replace('/sale', url)
            yield scrapy.Request(url=url, meta={'item': item},
                                 callback=self.parse_sub_area, dont_filter=True)

    def parse_sub_area(self, response):
        im = response.meta['item']
        nodes = response.css('.quyun-box-more dd a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = extract(node.css('::text'))
            if name == '不限':
                continue
            if not config_repo.exist(item['source'], name):
                item['sub_area'] = name
                url = node.css('::attr(href)').extract_first()
                url = re.sub('/sale/[a-zA-Z0-9]*/*', url, response.url)
                item['sub_area_url'] = url
                yield item
