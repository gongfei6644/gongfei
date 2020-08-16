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


class FangCitiesCommunitySpider(scrapy.Spider):
    name = 'fang_cities_community'
    allowed_domains = ['www.fang.com']
    start_urls = ['https://esf.fang.com/newsecond/esfcities.aspx']
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CityPipeline': 300,
        }
    }

    def parse(self, response):
        nodes = response.xpath('//li[contains(@class, "blubk")]/a')
        for node in nodes:
            item = CityItem()
            city = node.xpath('string(./text())').extract_first().strip()
            source = SITE_FANG_COMMUNITY
            city = get_full_city_name(city)
            # # 先删除原始数据
            # config_repo.delete(source, city)

            href = node.xpath('string(./@href)').extract_first().strip()
            url = "https:" + href + "/housing/__1_0_0_0_1_0_0_0/"
            item['city'] = city
            item['source'] = source
            headers = {
                "User-Agent":  "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
                "Referer": "http://search.fang.com/captcha-verify/redirect?h={}".format(url)}
            yield scrapy.Request(
                url=url, meta={'item': item}, callback=self.parse_area, headers=headers, dont_filter=True)

    def parse_area(self, response):
        print([response.status, response.url])
        im = response.meta['item']
        nodes = response.xpath('//div[@class="qxName"]/a')
        for node in nodes:
            item = copy.deepcopy(im)
            name = node.xpath('string(./text())').extract_first().strip()
            if not any(["周边" in name, "旅游" in name, "风景" in name,
                "名胜" in name, "其他" in name, "其它" in name, "不限" in name, "周边" in name]):
                item['area'] = name
                href = node.xpath('string(./@href)').extract_first().strip()
                url = urljoin(response.url, href)
                headers = {
                    "User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
                    "Referer": "http://search.fang.com/captcha-verify/redirect?h={}".format(url)}
                yield scrapy.Request(url=url, meta={'item': item},
                    callback=self.parse_sub_area, headers=headers, dont_filter=True)

    def parse_sub_area(self, response):
        im = response.meta['item']
        nodes = response.xpath('//p[@id="shangQuancontain"]/a')
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
