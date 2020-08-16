# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import base64
import logging
import random
import time
from datetime import datetime

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.repository.case_repo import CaseRepo
from FxtDataAcquisition.repository.project_info_repo import ProjectInfoRepo
from FxtDataAcquisition.settings import *
from FxtDataAcquisition.utils.redis_client import rediz

logger = logging.getLogger(__name__)
conf_repo = ConfigRepo()
case_repo = CaseRepo()
pinfo_repo = ProjectInfoRepo()


class ProxySpiderMiddleware(object):

    def process_request(self, request, spider):
        provider = PROXY['provider']
        # r = random.choices([0, 1], [4, 6])[0]
        # if r == 1 and provider:
        proxy_user = PROXY['user']
        proxy_pass = PROXY['password']
        if provider == 'dailiyun':
            proxy_server = 'http://' + self.get_proxy()
            proxy_auth = "Basic " + proxy_user + ":" + proxy_pass
        else:
            proxy_server = PROXY['proxy_server']
            proxy_auth = "Basic " + base64.urlsafe_b64encode(
                bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")
        logger.info('{} spider: {} use proxy is {}'.format(datetime.now(), spider.name, proxy_server))

        request.meta["proxy"] = proxy_server
        request.headers["Proxy-Authorization"] = proxy_auth
        request.headers["User-Agent"] = random.choice(UA_LIST)

    def get_proxy(self):
        result = rediz.hgetall(PROXY['redis_key'])
        if result:
            return random.choice(list(result.keys()))
        else:
            return self.get_proxy()


class ExceptionMiddleware(object):

    def process_response(self, request, response, spider):
        if response.status == 404:
            if spider.name.__contains__('community'):
                pinfo_repo.update_status(None, status=0, remark='404', url=response.url)
            else:
                conf = conf_repo.get_detail(None, response.url)
                if conf:
                    case_repo.update_status(None, conf['city'], status=0, remark='404', url=response.url)
        # logger.warning('{} occurred http status is: {}! spider is: {}, request url: {}'
        #                 .format(datetime.now(), response.status, spider.name, request.url))
        return response

    def process_exception(self, request, exception, spider):
        logger.error('{} occurred exception! spider is: {}'.format(datetime.now(), spider.name), exception)
        # if isinstance(exception, TimeoutError):
        #     print()
        pass


class TooManyRequestsRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        req_url = request.url
        allowed_domains = spider.allowed_domains
        if "verify" in req_url:
            time.sleep(RETRY_DELAY)

        if request.meta.get('dont_retry', False) and "verify" not in response.url:
            return response
        elif response.status == 429 and "verify" not in req_url:
            if self.is_allowed_domains(req_url, allowed_domains):
                time.sleep(RETRY_DELAY)  # If the rate limit is renewed in a minute, put 60 seconds, and so on.
                reason = response_status_message(response.status)
                # 对于429状态的请求，尽量保证能正常请求到数据
                request.meta["max_retry_times"] = S29_RETRY_TIMES
                return self._retry(request, reason, spider) or response
        elif response.status in self.retry_http_codes:
            if self.is_allowed_domains(req_url, allowed_domains):
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response
        return response

    def is_allowed_domains(self, req_url, allowed_domains):
        for domain in allowed_domains:
            if req_url.__contains__(domain.replace('www.', '')):
                return True
        return False


class FxtdataacquisitionSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FxtdataacquisitionDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
