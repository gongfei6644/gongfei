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
from FxtDataAcquisition.settings import SITE_CITYHOUSE_COMMUNITY

config_repo = ConfigRepo()


class CityhouseCitiesCommunitySpider(scrapy.Spider):
    name = 'cityhouse_cities_community'
    allowed_domains = ['www.cityhouse.cn']
    start_urls = ['http://www.cityhouse.cn/city.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CityPipeline': 300,
        }
    }

    def parse(self, response):
        nodes = response.xpath('//div[@class="le_list"]//a')
        for node in nodes:
            item = CityItem()
            city = node.xpath('./text()').extract_first().strip()
            source = SITE_CITYHOUSE_COMMUNITY
            city = get_full_city_name(city)
            # # 先删除原始数据
            # config_repo.delete(source, city)

            href = node.xpath('./@href').extract_first().strip()
            url = urljoin(href, '/ha/dsTL-pr11-in2/')
            item['city'] = city
            item['source'] = source
            yield scrapy.Request(url=url, meta={'item': item},
                                 callback=self.parse_area, dont_filter=True)

    def parse_area(self, response):
        """
        没有片区,直接把行政区信息存入片区字段
        :param response:
        :return:
        """
        im = response.meta['item']
        nodes = response.xpath('//div[@class="so_cont"][1]/ul[@class="so_cont_term"]//a')[2:]
        for node in nodes:
            item = copy.deepcopy(im)
            name = node.xpath('./text()').extract_first().strip()
            if not config_repo.exist(item['source'], name):
                item['area'] = name
                href = node.xpath('./@href').extract_first().strip()
                url = urljoin(response.url, href)
                item["sub_area"] = name
                item["sub_area_url"] = url

                yield item




