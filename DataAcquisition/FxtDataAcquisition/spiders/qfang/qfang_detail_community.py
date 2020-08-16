# -*- coding: utf-8 -*-
# @Time    : 2019-05-23 10:55
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
    ret = case_service.get_raw_case(SITE_QFANG_COMMUNITY)
    return ret


first_case = get_case()


class QfangDetailCommunitySpider(scrapy.Spider):
    name = 'qfang_detail_community'
    allowed_domains = ['www.qfang.com']
    start_urls = [first_case.get('source_link', None)]
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        node = response.xpath('//div[@class="head-info-field garden fl clearfix"]')
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
            pinfo_repo.update_status(_id)
        case = get_case()
        if case:
            yield scrapy.Request(url=case.get('source_link', None), meta={'brief': case},
                                 callback=self.parse, dont_filter=True)

    def parse_page(self, item, node, response):
        item["停车位"] = node.xpath('string(.//em[contains(text(), "停")]/parent::span[1]/following-sibling::p[1]/text())').extract_first()
        item["总户数"] = node.xpath('string(.//em[contains(text(), "户")]/parent::span[1]/following-sibling::p[1]/text())').extract_first()
        item["物业费"] = node.xpath('string(.//em[contains(text(), "物")]/parent::span[1]/following-sibling::p[1]/text())').extract_first()
        item["单元总数"] = node.xpath('string(.//span[contains(text(), "单元总数")]/following-sibling::*[1]/text())').extract_first()
        item["物业公司"] = node.xpath('string(.//span[contains(text(), "物业公司")]/following-sibling::*[1]/text())').extract_first()
        item["开发商"] = node.xpath('string(.//span[contains(text(), "开 发 商")]/following-sibling::*[1]/text())').extract_first()
        item["小区坐标"] = self.get_position(response)
        return item

    @staticmethod
    def get_position(response):
        try:
            lon = response.xpath('.').re(r'longitude="([\d\\.]+)"')
            lat = response.xpath('.').re(r'latitude="([\d\\.]+)"')
            position = "{},{}".format(lon[0], lat[0])
            return position
        except Exception as e:
            logger.error("获取小区坐标异常{} {}".format(e, traceback.format_exc()))

