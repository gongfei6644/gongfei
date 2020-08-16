# -*- coding: utf-8 -*-
# @Time    : 2019-05-29 15:55
# @Author  : luomingming
# @Desc    :

import copy
import os

import scrapy

from FxtDataAcquisition.items import CityItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.spiders.common import *

config_repo = ConfigRepo()


class WBCitiesCommunitySpider(scrapy.Spider):
    name = '58_cities_community'
    allowed_domains = ['www.58.com']
    start_urls = ['https://www.58.com/changecity.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CityPipeline': 300,
        }
    }

    def parse(self, response):
        json_file = os.path.join(os.path.dirname(__file__), "58citylist.json")
        with open(json_file, "r", encoding='utf-8') as file:
            data = file.read()
            city_list = json.loads(data, encoding='utf-8')
            for _, cities in city_list.items():
                for city, value in cities.items():
                    city_param = value.split('|')
                    city_code = city_param[0]
                    url = "https://{}.58.com/xiaoqu/".format(city_code)

                    source = SITE_58_COMMUNITY
                    city = get_full_city_name(city)
                    # # 先删除原始数据
                    # config_repo.delete(source, city)

                    item = CityItem()
                    item['city'] = city
                    item['source'] = source
                    yield scrapy.Request(url=url, meta={'item': item},
                                         callback=self.parse_area, dont_filter=True)

    def parse_area(self, response):
        im = response.meta['item']
        nodes = response.css('.filter-wrap dl:nth-child(1) dd a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = extract(node.css('::text'))
            if name == '不限':
                continue
            item['area'] = name
            url = response.url + extract(node.css('::attr(value)'))
            yield scrapy.Request(url=url, meta={'item': item},
                                 callback=self.parse_sub_area, dont_filter=True)

    def parse_sub_area(self, response):
        im = response.meta['item']
        nodes = response.css('.filter-wrap dl:nth-child(2) dd div a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = extract(node.css('::text'))
            if name == '不限':
                continue
            if not config_repo.exist(item['source'], name):
                item['sub_area'] = name
                url = response.url
                item['sub_area_url'] = url[:url.index('xiaoqu/') + 7] + extract(node.css('::attr(value)')) + '/'
                yield item
