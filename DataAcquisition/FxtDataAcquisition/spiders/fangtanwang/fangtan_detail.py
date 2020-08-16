# -*- coding: utf-8 -*-
# @Time    : 2019-04-18 15:47
# @Author  : luomingming
# @Desc    : 详情

import scrapy
import logging
from datetime import datetime
import re
from copy import copy
from FxtDataAcquisition.items import CaseItem
from FxtDataAcquisition.repository.case_repo import CaseRepo
from FxtDataAcquisition.service.case_service import CaseService
from FxtDataAcquisition.spiders.common import *
from FxtDataAcquisition.settings import SITE_FANGTAN

logger = logging.getLogger(__name__)
case_repo = CaseRepo()
case_service = CaseService(case_repo)


def get_case():
    ret = case_service.get_raw_case(SITE_FANGTAN)
    return ret


first_case = get_case()


class FangtanDetailSpider(scrapy.Spider):
    name = 'fangtan_detail'
    allowed_domains = ['www.fangtan007.com']
    start_urls = [first_case.get('source_link', None)]
    custom_settings = {
        # 'CONCURRENT_REQUESTS': 16,
        # 'LOG_LEVEL': "DEBUG",
        # 'LOG_FILE': LOG_PATH + "fangtan_detail.log",
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CasePipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        node = response.css(".fang-info-jb")
        meta = copy(response.meta)
        if 'brief' in meta.keys():
            brief = meta['brief']
        else:
            brief = first_case
        _id = brief.get('_id', None)
        city = brief['city']
        if node:
            item = CaseItem()
            item['_id'] = _id
            item['d_status'] = 1
            item['detail_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['case_type_code'] = '3001001'
            item['data_source'] = brief['data_source']
            item['city'] = brief['city']
            self.parse_page(item, node, response)
            # 字段统计
            statis_detail(item)
            yield item
        else:
            case_repo.update_status(_id, city, remark='页面无数据')
        case = get_case()
        if case:
            yield scrapy.Request(url=case.get('source_link', None), meta={'brief': case},
                                 callback=self.parse, dont_filter=True)

    def parse_page(self, item, node, response):
        jba = node.xpath("./ul[@class='jba']")
        item['total_price'] = extract(jba.xpath("./li[1]/span[1]/b/text()"))
        tmp = jba.xpath("./li[2]/*/text()").extract()
        item['project_name'] = tmp[0].strip()
        if len(tmp) == 2:
            item['house_area'] = re.match('\d+', tmp[1]).group()
        if len(tmp) == 3:
            item['house_type'] = tmp[2].strip()
        tmp = node.xpath("./ul[@class='jbb']/li/text()").extract()
        for v in tmp:
            s = v.split('：')
            key = s[0].strip()
            value = s[1].strip()
            if key == '朝向':
                item['orientation'] = value
            if key == '装修':
                item['decoration'] = value
            if key == '建造':
                item['build_date'] = value
            if key == '楼层':
                m = re.findall('\d+', v)
                item['floor_no'] = m[0]
                item['total_floor_num'] = m[1]
        jbc = node.xpath("./ul[@class='jbc']/li")
        peitao = None
        for nod in jbc:
            v = extract(nod.xpath("text()"))
            s = v.split('：')
            if len(s) == 1:
                s = v.split(':')
            key = s[0].strip()
            value = s[1].strip()
            if key == '类型':
                item['usage'] = value
                continue
            if key == '地址':
                item['address'] = extract(nod.xpath("./a/text()"))
                continue
            if key == '配套':
                pt = nod.xpath("./span/text()").extract()
                if pt:
                    pt = '-'.join(pt)
                    m = re.match('[\u4e00-\u9fa5]', pt)
                    if m:
                        peitao = pt
                continue
        item['tel'] = extract(node.xpath("./div[@class='tel']/span/text()"))
        if not peitao:
            desc = response.css(".fang-detail-info span::text").extract()
            if desc:
                peitao = ";".join(desc)
        if peitao:
            if peitao.__contains__('电梯'):
                item['supporting_facilities'] = '电梯'
                item['is_elevator'] = '有'
            else:
                item['is_elevator'] = '无'















