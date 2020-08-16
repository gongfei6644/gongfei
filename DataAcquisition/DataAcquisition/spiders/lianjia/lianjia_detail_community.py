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
    ret = case_service.get_raw_case(SITE_LIANJIA_COMMUNITY)
    return ret


first_case = get_case()


class LianjiaDetailCommunitySpider(scrapy.Spider):
    name = 'lianjia_detail_community'
    allowed_domains = ['www.lianjia.com']
    start_urls = [first_case.get('source_link', None)]
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        node = response.xpath('//span[@class="xiaoquUnitPrice"]')
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
        item["地址"] = response.xpath('string(//div[@class="detailDesc"]/text())').extract_first().strip()
        item["建筑年代"] = response.xpath('string(//*[text()="建筑年代"]/following-sibling::*[1]/text())').extract_first().strip()
        item["建筑类型"] = response.xpath('string(//*[text()="建筑类型"]/following-sibling::*[1]/text())').extract_first().strip()
        item["物业费用"] = response.xpath('string(//*[text()="物业费用"]/following-sibling::*[1]/text())').extract_first().strip()
        item["物业公司"] = response.xpath('string(//*[text()="物业公司"]/following-sibling::*[1]/text())').extract_first().strip()
        item["开发商"] = response.xpath('string(//*[text()="开发商"]/following-sibling::*[1]/text())').extract_first().strip()
        item["楼栋总数"] = response.xpath('string(//*[text()="楼栋总数"]/following-sibling::*[1]/text())').extract_first().strip()
        item["户数"] = response.xpath('string(//*[text()="房屋总数"]/following-sibling::*[1]/text())').extract_first().strip()

        item["小区坐标"] = self.get_position(response)

        return item

    @staticmethod
    def get_position(response):
        try:
            position1 = response.xpath('.').re(r'xiaoqu="\[(.*)\]"')
            position2 = response.xpath('.').re(r"resblockPosition:'([\d\\.,]+)'")
            position = (position1 or position2)[0]
            return position
        except Exception as e:
            logger.error("获取小区坐标异常{} {}".format(e, traceback.format_exc()))
            raise ValueError("获取坐标异常")