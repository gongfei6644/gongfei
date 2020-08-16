# -*- coding: utf-8 -*-
# @Time    : 2019-04-30 10:05
# @Author  : luomingming
# @Desc    :

import scrapy
import logging
import re
import traceback
from copy import copy
from datetime import datetime, timedelta
from FxtDataAcquisition.items import CaseItem
from FxtDataAcquisition.repository.case_repo import CaseRepo
from FxtDataAcquisition.service.case_service import CaseService
from FxtDataAcquisition.spiders.common import *
from FxtDataAcquisition.settings import SITE_HOUSE365

logger = logging.getLogger(__name__)
case_repo = CaseRepo()
case_service = CaseService(case_repo)


def get_case():
    ret = case_service.get_raw_case(SITE_HOUSE365)
    return ret


first_case = get_case()


class House365DetailSpider(scrapy.Spider):
    name = 'house365_detail'
    allowed_domains = ['www.house365.com']
    start_urls = [first_case.get('source_link', None)]
    custom_settings = {
        # 'CONCURRENT_REQUESTS': 16,
        'REDIRECT_ENABLED': False,
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.CasePipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        node = response.css(".person_info_fl")
        if not node:
            node = response.css(".houseInfo .houseInfoMain")
        meta = copy(response.meta)
        if 'brief' in meta.keys():
            brief = meta['brief']
        else:
            brief = first_case
        _id = brief.get('_id', None)
        city = brief['city']
        if node:
            date_interval = extract(node.xpath("./p[@class='showtimer']/span[3]/text()"))
            if not date_interval:
                date_interval = extract(node.xpath("./div[1]/text()"))
            r = compute_case_date(date_interval)
            is_last_month = r[0]
            case_happen_date = r[1]
            if is_last_month:
                case_repo.update_status(_id, city, status=2)
            elif case_happen_date:
                item = CaseItem()
                item['_id'] = _id
                item['d_status'] = 1
                item['case_happen_date'] = case_happen_date
                item['detail_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                item['case_type_code'] = '3001001'
                item['data_source'] = brief['data_source']
                item['city'] = brief['city']
                self.parse_page(item, node)

                statis_detail(item)
                yield item
        else:
            case_repo.update_status(_id, city, remark='页面无数据')
        case = get_case()
        if case:
            yield scrapy.Request(url=case.get('source_link', None), meta={'brief': case},
                                 callback=self.parse, dont_filter=True)

    def parse_page(self, item, node):
        info_node = node.css(".person_info .gr_table dl")
        if not info_node:
            info_node = node.xpath("./dl")
        for el in info_node:
            t = extract(el.xpath("./dt/text()"))
            v = extract(el.xpath("./dd/text()"))
            if t.__contains__('售价'):
                item['total_price'] = extract(el.xpath("./dd/span/i/text()"))
            elif t.__contains__('总价'):
                item['total_price'] = extract(el.xpath("./dd/span[1]/text()"))
            elif t.__contains__('户型'):
                item['house_type'] = v
            elif t.__contains__('楼层'):
                s = v.split('/')
                item['floor_no'] = s[0]
                item['total_floor_num'] = s[1]
            elif t.__contains__('朝向'):
                item['orientation'] = v
            elif t.__contains__('类型'):
                item['usage'] = v
            elif t.__contains__('装修'):
                item['decoration'] = v
            elif t.__contains__('权属'):
                item['property_nature'] = v
            elif t.__contains__('年代'):
                item['build_date'] = v
            elif t.__contains__('小区'):
                project_name = extract(el.xpath("./dd/a[1]/text()"))
                if not project_name:
                    project_name = extract(el.xpath("./dd/div/a[1]/text()"))
                if not project_name:
                    project_name = extract(el.xpath("./dd/div/text()"))
                if not project_name:
                    project_name = extract(el.xpath("./dd/span/text()"))
                if project_name:
                    item['project_name'] = project_name
        tel = extract(node.css(".person_info .gr_tell .tell-num::text"))
        if not tel:
            tel = extract(node.css(".telephoneBox div::text"))
        if tel:
            item['tel'] = tel.replace(' ', '')
        address = extract(node.css("#zbxx_cont div p:nth-child(1)::text"))
        if address:
            address = address.split('：')[1]
        else:
            address = extract(node.xpath("//div[@id='zbss']/div[2]/div/dl/dd/text()"))
        if address:
            item['address'] = address
        fwxq = node.css(".person_cont #fwxq_cont div div:nth-child(1)")
        if fwxq:
            fwxq = extract(fwxq.css("*::text"))
            fwxq = re.sub('\s', '', fwxq)
            if fwxq.__contains__('电梯'):
                item['supporting_facilities'] = '电梯'
                item['is_elevator'] = '有'
            else:
                item['is_elevator'] = '无'















