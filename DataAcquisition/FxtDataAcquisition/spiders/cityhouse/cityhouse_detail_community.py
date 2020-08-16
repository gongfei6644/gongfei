# -*- coding: utf-8 -*-
# @Time    : 2019-05-23 10:55
# @Author  : luomingming
# @Desc    :

from copy import copy, deepcopy
from urllib.parse import urljoin

import requests
import scrapy
from lxml import etree
from requests.exceptions import ProxyError

from FxtDataAcquisition.items import ProjectInfoItem
from FxtDataAcquisition.repository.project_info_repo import ProjectInfoRepo
from FxtDataAcquisition.service.case_service import CaseService
from FxtDataAcquisition.spiders.common import *


logger = logging.getLogger(__name__)
pinfo_repo = ProjectInfoRepo()
case_service = CaseService(pinfo_repo)


def get_case():
    ret = case_service.get_raw_case(SITE_CITYHOUSE_COMMUNITY)
    return ret


first_case = get_case()



class CityhouseDetailCommunitySpider(scrapy.Spider):
    name = 'cityhouse_detail_community'
    allowed_domains = ['www.cityhouse.cn']
    start_urls = [first_case.get('source_link', None)]
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        node = response.xpath('//div[@class="cont clearfix"]')
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
        item["用途"] = node.xpath('.//*[contains(text(), "用途")]/following-sibling::*[1]/span/text()').extract_first()
        item["开发商"] = node.xpath('.//*[contains(text(), "开发商")]/following-sibling::*[1]/a/@title').extract_first()
        item["物业公司"] = node.xpath('string(.//*[contains(text(), "物业公司")]/parent::*[1]/text())').extract_first().strip()
        greening = node.xpath('.//*[contains(text(), "绿化率")]/following-sibling::*[1]/text()').re('[\d%\.%]+')
        item["绿化率"] = greening[0] if greening else None
        volume = node.xpath('.//*[contains(text(), "容积率")]/following-sibling::*[1]/text()').re('[\d%\.]+')
        item["容积率"] = volume[0] if volume else None
        item["占地面积"] = node.xpath('.//*[contains(text(), "占地面积")]/following-sibling::*[1]/text()').extract_first().strip()
        item["建筑面积"] = node.xpath('.//*[contains(text(), "建筑面积")]/following-sibling::*[1]/text()').extract_first().strip()
        item["开盘时间"] = node.xpath('.//*[contains(text(), "开盘时间")]/following-sibling::*[1]/text()').extract_first().strip()
        item["竣工时间"] = node.xpath('.//*[contains(text(), "竣工时间")]/following-sibling::*[1]/text()').extract_first().strip()
        item["综合评分"] = response.xpath('string(//span[@class="eval"]/span/text())').extract_first().strip()
        item["在售套数"] = self.get_case_num(response)
        item["小区坐标"] = self.get_position(response)
        return item

    @staticmethod
    def get_case_num(response):
        case_num_href = response.xpath('string(//a[contains(text(), "新增出售")]/@href)').extract_first()
        case_num_url = urljoin(response.url, case_num_href)
        proxy = "http://{}:{}@{}".format(PROXY["user"], PROXY["password"], PROXY["proxy_server"].replace("http://", ""))
        proxies = {"http": proxy, "https": proxy}
        headers = deepcopy(DEFAULT_REQUEST_HEADERS)
        headers.update({"referer": response.url})
        for i in range(RETRY_TIMES):
            try:
                resp = requests.get(case_num_url, headers=headers, proxies=proxies, timeout=30, verify=False)
                html = etree.HTML(resp.text)
                case_num = html.xpath('string(//a[contains(text(), "新增")]/span/text())')
                return case_num
            except ProxyError:
                pass
            except Exception as e:
                logger.info("在售案例异常{}, {}".format(e, traceback.format_exc()))

    @staticmethod
    def get_position(response):
        r = response.xpath('.').re(r'haXy=([\d\\|\\.]+)')
        position = r[0].replace("|", ",") if r else ""
        return position

