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
    ret = case_service.get_raw_case(SITE_FANG_COMMUNITY)
    return ret


first_case = get_case()


class FangDetailCommunitySpider(scrapy.Spider):
    name = 'fang_detail_community'
    allowed_domains = ['www.fang.com']
    start_urls = [first_case.get('source_link', None)]
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300},
        'LOG_PATH': '/usr/local/DataCollection/logs/FxtDataAcquisition/{}'.format(name)
    }

    def start_requests(self):
        for url in self.start_urls:
            headers = {
                "User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
                "Referer": "http://search.fang.com/captcha-verify/redirect?h={}".format(url)}
            yield scrapy.Request(url=url, callback=self.parse, headers=headers, dont_filter=True)

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        node = response.xpath('//div[@class="Rinfolist"]')
        meta = copy(response.meta)
        if 'brief' in meta.keys():
            brief = meta['brief']
        else:
            brief = first_case
        _id = brief.get('_id', None)
        if node:
            item = ProjectInfoItem()
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
        item["小区地址"] = response.xpath('string(//*[contains(text(), "小区地址")]/parent::*[1]/text())').extract_first().strip()
        item["产权描述"] = response.xpath('string(//*[contains(text(), "产权描述")]/parent::*[1]/text())').extract_first().strip()
        item["建筑年代"] = response.xpath('string(//*[contains(text(), "建筑年代")]/parent::8[1]/text())').extract_first().strip()
        item["建筑类型"] = response.xpath('string(//*[contains(text(), "建筑类型")]/parent::*[1]/text())').extract_first().strip()
        item["建筑结构"] = response.xpath('string(//*[contains(text(), "建筑结构")]/parent::*[1]/text())').extract_first().strip()
        item["建筑面积"] = response.xpath('string(//*[contains(text(), "建筑面积")]/parent::*[1]/text())').extract_first().strip()
        item["占地面积"] = response.xpath('string(//*[contains(text(), "占地面积")]/parent::*[1]/text())').extract_first().strip()
        item["楼栋总数"] = response.xpath('string(//*[contains(text(), "楼栋总数")]/parent::*[1]/text())').extract_first().strip()
        item["房屋总数"] = response.xpath('string(//*[contains(text(), "房屋总数")]/parent::*[1]/text())').extract_first().strip()
        item["绿化率"] = response.xpath('string(//*[contains(text(), "绿 化 率")]/parent::*[1]/text())').extract_first().strip()
        item["容积率"] = response.xpath('string(//*[contains(text(), "容 积 率")]/parent::*[1]/text())').extract_first().strip()
        item["开发商"] = response.xpath('string(//*[contains(text(), "开 发 商")]/parent::*[1]/text())').extract_first().strip()
        item["物业费"] = response.xpath('string(//*[contains(text(), "物 业 费")]/parent::*[1]/text())').extract_first().strip()
        item["环线位置"] = response.xpath('string(//*[contains(text(), "环线位置")]/parent::*[1]/text())').extract_first().strip(": ")
        item["停车位"] = response.xpath('string(//*[contains(text(), "停 车 位")]/parent::*[1]/text())').extract_first().strip()
        item["物业公司"] = response.xpath('string(//*[contains(text(), "物业公司")]/parent::*[1]/text())').extract_first().strip()
        item["物业类别"] = response.xpath('string(//*[contains(text(), "物业类别")]/parent::*[1]/text())').extract_first().strip()
        item["物业电话"] = response.xpath('string(//*[contains(text(), "物业办公电话")]/parent::*[1]/text())').extract_first().strip()
        item["物业办公地点"] = response.xpath('string(//*[contains(text(), "物业办公地点")]/parent::*[1]/text())').extract_first().strip()
        item["电梯服务"] = response.xpath('string(//*[contains(text(), "电梯服务")]/parent::*[1]/text())').extract_first().strip()
        item["安全管理"] = response.xpath('string(//*[contains(text(), "安全管理")]/parent::*[1]/text())').extract_first().strip()
        traffic = response.xpath('//h3[contains(text(), "交通状况")]/parent::*[1]/following-sibling::*[1]//text()').extract()
        item["交通状况"] = re.sub(r'\s', '', "".join(traffic))
        item["小区评级"], item["活跃度评级"], item["板块评级"], item["物业评级"], item["教育评级"] = self.get_level(response)
        item["小区坐标"] = self.get_position(response)

        return item

    @staticmethod
    def get_level(response):
        level_url = response.url.replace("com/xiangqing", "com/pingji")
        proxy = "http://{}:{}@{}".format(PROXY["user"], PROXY["password"], PROXY["proxy_server"].replace("http://", ""))
        proxies = {"http": proxy, "https": proxy}
        headers = deepcopy(DEFAULT_REQUEST_HEADERS)
        headers.update({"referer": response.url})
        for i in range(RETRY_TIMES):
            try:
                resp = requests.get(level_url, headers=headers, proxies=proxies, timeout=30, verify=False)
                text = resp.content.decode("gb2312", "ignore")
                html = etree.HTML(text)
                stars = html.xpath('string(//div[@class="star_group fl"]//p[contains(@class, "ls_star ls_red_ red_s")]/@class)').strip('ls_star ls_red_ red_s')
                stars = int(stars)/2
                activity_level = html.xpath('string(//span[text()="活跃度评级"]/following-sibling::*[1]/text())')
                plate_level = html.xpath('string(//span[text()="板块评级"]/following-sibling::*[1]/text())')
                property_level = html.xpath('string(//span[text()="物业评级"]/following-sibling::*[1]/text())')
                edu_level = html.xpath('string(//span[text()="教育评级"]/following-sibling::*[1]/text())')
                return stars, activity_level, plate_level, property_level, edu_level
            except ProxyError:
                pass
            except Exception as e:
                logger.info("小区评级异常{}, {}".format(e, traceback.format_exc()))

    @staticmethod
    def get_position(response):
        host = response.xpath('string(//a[text()="房天下"]/following-sibling::a[1]/@href)')
        new_code = response.xpath(r'string(//*[@id="xqwxqy_B03_19"]/@src)').split("newcode=")[-1]
        map_url = "http:" + host + "/newsecond/map/NewHouse/NewProjMap.aspx?newcode=" + new_code
        proxy = "http://{}:{}@{}".format(PROXY["user"], PROXY["password"], PROXY["proxy_server"].replace("http://", ""))
        proxies = {"http": proxy, "https": proxy}
        headers = deepcopy(DEFAULT_REQUEST_HEADERS)
        headers.update({"referer": response.url})
        for i in range(RETRY_TIMES):
            try:
                resp = requests.get(map_url, headers=headers, proxies=proxies, timeout=30, verify=False)
                text = resp.content.decode("gb", "ignore")
                position_str = re.findall(r'mapInfo=({.*})', text)
                if position_str:
                    zoom = "zoom"
                    mapZoom = "mapZoom"
                    px = "px"
                    py = "py"
                    isKey = "isKey"
                    try:
                        position_map = eval(position_str[0])
                        px = position_map["px"]
                        py = position_map["py"]
                    except:
                        pass
                    else:
                        return "{},{}".format(px, py)
            except ProxyError:
                pass
            except Exception as e:
                logger.info("小区坐标异常{}, {}".format(e, traceback.format_exc()))
