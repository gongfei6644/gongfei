# -*- coding: utf-8 -*-
# @Time    : 2019-05-23 10:55
# @Author  : luomingming
# @Desc    :

from copy import copy, deepcopy

import requests
import scrapy
from requests.exceptions import ProxyError

from FxtDataAcquisition.items import ProjectInfoItem
from FxtDataAcquisition.repository.project_info_repo import ProjectInfoRepo
from FxtDataAcquisition.service.case_service import CaseService
from FxtDataAcquisition.spiders.common import *

logger = logging.getLogger(__name__)
pinfo_repo = ProjectInfoRepo()
case_service = CaseService(pinfo_repo)


def get_case():
    ret = case_service.get_raw_case(SITE_ANJUKE_COMMUNITY)
    return ret


first_case = get_case()


class AnjukeDetailCommunitySpider(scrapy.Spider):
    name = 'anjuke_detail_community'
    allowed_domains = ['www.anjuke.com']
    start_urls = [first_case.get('source_link', None)]
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}, 代理: {}'.format(datetime.now(), response.url, response.meta['proxy']))
        # 测试：如果没有使用代理则抛异常退出
        # if not response.meta['proxy']:
        #     raise Exception('no proxy')
        node = response.xpath('//dl[@class="basic-parms-mod"]')
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
        item["物业类型"] = node.xpath('string(.//*[contains(text(), "物业类型")]/following-sibling::*[1]/text())').extract_first().strip()
        item["建筑面积"] = node.xpath('string(.//*[contains(text(), "总建面积")]/following-sibling::*[1]/text())').extract_first().strip()
        item["建筑年代"] = node.xpath('string(.//*[contains(text(), "建造年代")]/following-sibling::*[1]/text())').extract_first().strip()
        item["容积率"] = node.xpath('string(./dt[contains(text(), "容")]/following-sibling::*[1]/text())').extract_first().strip()
        item["开发商"] = node.xpath('string(./dt[contains(text(), "开")]/following-sibling::*[1]/text())').extract_first().strip()
        item["物业公司"] = node.xpath('string(./*[contains(text(), "物业公司")]/following-sibling::*[1]/text())').extract_first().strip()
        item["学区"] = node.xpath('string(./dt[contains(text(), "学")]/following-sibling::*[1]/text())').extract_first().strip()
        item["总户数"] = node.xpath('string(./*[contains(text(), "总户数")]/following-sibling::*[1]/text())').extract_first().strip()
        item["停车位"] = node.xpath('string(./*[contains(text(), "停车位")]/following-sibling::*[1]/text())').extract_first().strip()
        item["绿化率"] = node.xpath('string(./*[contains(text(), "绿化率")]/following-sibling::*[1]/text())').extract_first().strip()
        item["在售案例"] = self.get_case_num(response)
        item["小区坐标"] = self.get_position(response)
        return item

    @staticmethod
    def get_case_num(response):
        proxy = "http://{}:{}@{}".format(PROXY["user"], PROXY["password"], PROXY["proxy_server"].replace("http://", ""))
        proxies = {"http": proxy, "https": proxy}
        commid = response.url[response.url.rindex('/') + 1:]
        case_num_url = 'https://wuhan.anjuke.com/v3/ajax/communityext/?commid={}&useflg=onlyForAjax'.format(commid)
        headers = deepcopy(DEFAULT_REQUEST_HEADERS)
        headers.update({"referer": response.url})
        for i in range(RETRY_TIMES):
            try:
                r = requests.get(case_num_url, headers=headers, proxies=proxies, timeout=30, verify=False)
                if r.status_code == 200:
                    j = json.loads(r.text)
                    case_num = j['comm_propnum']['saleNum']
                    return case_num
            except ProxyError:
                pass
            except Exception as e:
                logger.info("在售案例异常{}, {}".format(e, traceback.format_exc()))

    @staticmethod
    def get_position(response):
        try:
            lng = response.re(r'lng: "([\d\\.]+)",')
            lat = response.re(r'lat: "([\d\\.]+)",')
            position = "{},{}".format(lng[0], lat[0])
            return position
        except Exception as e:
            logger.error("获取小区坐标异常{} {}".format(e, traceback.format_exc()))
