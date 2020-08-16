# -*- coding: utf-8 -*-
# @Time    : 2019-05-31 11:05
# @Author  : luomingming
# @Desc    :

from copy import copy

import requests
import scrapy

from FxtDataAcquisition.items import ProjectInfoItem
from FxtDataAcquisition.repository.project_info_repo import ProjectInfoRepo
from FxtDataAcquisition.service.case_service import CaseService
from FxtDataAcquisition.spiders.common import *

logger = logging.getLogger(__name__)
pinfo_repo = ProjectInfoRepo()
case_service = CaseService(pinfo_repo)


def get_case():
    ret = case_service.get_raw_case(SITE_58_COMMUNITY)
    return ret


first_case = get_case()


class WBDetailCommunitySpider(scrapy.Spider):
    name = '58_detail_community'
    allowed_domains = ['www.58.com']
    start_urls = [first_case.get('source_link', None)]
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        node = response.css(".info-container")
        meta = copy(response.meta)
        if 'brief' in meta.keys():
            brief = meta['brief']
        else:
            brief = first_case
        _id = brief.get('_id', None)
        if node:
            item = {}
            item['_id'] = _id
            item['d_status'] = 1
            item['detail_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item = self.parse_page(item, node, response)

            yield item
        else:
            pinfo_repo.update_status(_id, remark='页面无数据')
        case = get_case()
        if case:
            yield scrapy.Request(url=case.get('source_link', None), meta={'brief': case},
                                 callback=self.parse, dont_filter=True)

    def parse_page(self, item, node, response):
        item["小区均价"] = extract(node.css(".price-container .price::text"))
        case_num = node.xpath('.//*[text()="在售房源"]/following-sibling::*[1]//text()').re(r'(\d+)套')
        item["地址"] = node.xpath('string(.//*[text()="详细地址"]/following-sibling::*[1]/text())').extract_first().strip()
        item["建筑类别"] = node.xpath('string(.//*[text()="建筑类别"]/following-sibling::*[1]/text())').extract_first().strip()
        item["产权类别"] = node.xpath('string(.//*[text()="产权类别"]/following-sibling::*[1]/text())').extract_first().strip()
        item["产权年限"] = node.xpath('string(.//*[text()="产权年限"]/following-sibling::*[1]/text())').extract_first().strip()
        item["建筑年代"] = node.xpath('string(.//*[text()="建筑年代"]/following-sibling::*[1]/text())').extract_first().strip()
        item["停车位"] = node.xpath('string(.//*[text()="停车位"]/following-sibling::*[1]/text())').extract_first().strip()
        item["物业公司"] = node.xpath('string(.//*[text()="物业公司"]/following-sibling::*[1]/text())').extract_first().strip()
        item["开发商"] = node.xpath('string(.//*[text()="开发商"]/following-sibling::*[1]/text())').extract_first().strip()
        item["总户数"] = node.xpath('string(.//*[text()="总住户数"]/following-sibling::*[1]/text())').extract_first().strip()
        item["物业费用"] = node.xpath('string(.//*[text()="物业费用"]/following-sibling::*[1]/text())').extract_first().strip()
        item["容积率"] = node.xpath('string(.//*[text()="容积率"]/following-sibling::*[1]/text())').extract_first().strip()
        item["绿化率"] = node.xpath('string(.//*[text()="绿化率"]/following-sibling::*[1]/text())').extract_first().strip()
        item["建筑面积"] = node.xpath('string(.//*[text()="建筑面积"]/following-sibling::*[1]/text())').extract_first().strip()
        item["环线位置"] = response.xpath('string(//span[@class="addr"]/text())').extract_first().strip()
        item['在售套数'] = case_num[0] if case_num else None
        item["小区坐标"] = self.get_position(response)
        return item

    @staticmethod
    def get_position(response):
        try:
            lon = response.xpath('.').re(r'lon: "([\d\\.]+)",')
            lat = response.xpath('.').re(r'lat: "([\d\\.]+)",')
            position = "{},{}".format(lon[0], lat[0])
            return position
        except Exception as e:
            logger.error("获取小区坐标异常{} {}".format(e, traceback.format_exc()))

