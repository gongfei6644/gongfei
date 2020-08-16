# -*- coding: utf-8 -*-
# @Time    : 2019-05-29 15:55
# @Author  : luomingming
# @Desc    :

from copy import copy

import scrapy

from FxtDataAcquisition.items import ProjectInfoItem
from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.spiders.common import *

logger = logging.getLogger(__name__)
config_repo = ConfigRepo()
urls = config_repo.get_all_urls(SITE_58_COMMUNITY)


class WBListCommunitySpider(scrapy.Spider):
    name = '58_list_community'
    allowed_domains = ['www.58.com']
    start_urls = urls
    custom_settings = {
        'ITEM_PIPELINES': {
            'FxtDataAcquisition.pipelines.ProjectInfoPipeline': 300,
        }
    }

    def parse(self, response):
        logger.info('{} 当前采集的网页: {}'.format(datetime.now(), response.url))
        conf = None
        if 'conf' in response.meta.keys():
            meta = copy(response.meta)
            conf = meta['conf']
        if not conf:
            conf = config_repo.get_detail(SITE_58_COMMUNITY, response.url)
        if conf:
            nodes = response.css('.xq-list-wrap li')
            for node in nodes:
                item = {}
                item['list_page_url'] = response.url
                item['data_source'] = conf.get('source')
                item['city'] = conf.get('city')
                item['行政区'] = conf.get('area')
                item['片区'] = conf.get('sub_area')
                item = self.parse_list(item, node)
                yield item
            if nodes:
                yield from self.parse_next_page(conf, response)

    def parse_list(self, item, node):
        pn = node.css('.list-info h2 a')
        project_name = extract(pn.css('::text'))
        detail_link = extract(pn.css('::attr(href)'))
        project_price = extract(node.css(".price .unit::text"))
        project_price = re.match('\d+', project_price).group()
        crt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = uuid([detail_link, project_price, crt_time[0:7].replace('-', '')])
        item['uid'] = uid
        item['crt_time'] = crt_time
        item['source_link'] = detail_link
        item['楼盘名称'] = project_name
        item['小区均价'] = project_price
        return item

    def parse_next_page(self, conf, response):
        url = response.url
        if url.__contains__('pn_'):
            s = url.split('pn_')
            url = s[0]
            page_num = s[1]
            page_num = int(re.match('\d+', page_num).group())
            if page_num < 100:
                page_num += 1
            else:
                page_num = None
        else:
            page_num = 2
        if page_num:
            next_url = url + '/pn_{}/'.format(page_num)
            logger.info('{} 获取下一页地址: {}'.format(datetime.now(), next_url))
            yield scrapy.Request(url=next_url, meta={'conf': conf}, callback=self.parse, dont_filter=True)
