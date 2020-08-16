
import time
import random
import requests
# from fake_useragent import UserAgent
from requests.exceptions import ProxyError

from setting import config
from requests import ConnectTimeout
from utils import common_dlyproxy


def product_download(logger):
    return KeDownload(logger)


def test_product_download(logger):
    return TestDownload(logger)


def test2_product_download(logger):
    return Test2Download(logger)


class Test2Download:
    """阿布云测试"""
    def __init__(self, logger):
        # ua = UserAgent().random
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        self.headers = {
            'User-Agent': self.ua,
            'Connection': 'close'
        }
        self.logger = logger

    def get_str(self, url, headers={}, encoding='utf-8'):
        if headers:
            self.headers.update(headers)
        self.headers["User-Agent"] = self.ua
        try:
            proxyurl = config.ABY_URI_TEST2
            # proxyurl = get_proxy_dly(self.logger)  #测试, 临时使用代理云
            response = requests.get(url, headers=self.headers, proxies={'http': proxyurl, 'https': proxyurl},
                                    timeout=30, verify=False)
            print(response.status_code)
            print("请求:", url)
            print("返回:", response.url)
        except ProxyError as e:
            self.logger.info('代理错误: ' + str(e))
            # time.sleep(1)
        except Exception as e:
            self.logger.info('其它错误：' + str(e))
            time.sleep(random.randint(1, 15))
            # self.get_str(self, url, headers={}, encoding='utf-8')
        else:
            if response.status_code == 404:
                result = {'str': '404', 'link': response.url}
                return result
            elif response.status_code == 200:
                html_str = response.content.decode(encoding, 'ignore')
                result = {'str': html_str, 'link': response.url}
                return result
            else:
                self.logger.info('下载错误， 状态码为:{}'.format(response.status_code))
                # self. get_str(self, url, headers={}, encoding='utf-8')


class KeDownload:
    """阿布云"""
    def __init__(self, logger):
        # ua = UserAgent().random
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        self.headers = {
            'User-Agent': self.ua,
            'Connection': 'close'
        }
        self.logger = logger

    def get_str(self, url, headers={}, encoding='utf-8'):

        # self.encoding = encoding
        if headers:
            self.headers.update(headers)
        self.headers["User-Agent"] = self.ua
        try:
            proxyurl = config.ABY_URI_DETAIL
            # proxyurl = get_proxy_dly(self.logger)  #测试, 临时使用代理云
            response = requests.get(url, headers=self.headers, proxies={'http': proxyurl, 'https': proxyurl},
                                    timeout=30, verify=False)
        except TimeoutError as e:
            self.logger.info('超时错误: ' + str(e))
            time.sleep(random.randint(1, 15))
            # time.sleep(1)
        except Exception as e:
            self.logger.info('其它错误：' + str(e))
            time.sleep(random.randint(1, 15))
            # self.get_str(self, url, headers=self.headers, encoding=encoding)
        else:
            # print()
            if response.status_code == 404:
                result = {'str': '404', 'link': response.url}
                return result
            elif response.status_code == 200:
                html_str = response.content.decode(encoding, 'ignore')
                result = {'str': html_str, 'link': response.url}
                return result
            else:
                self.logger.info('下载错误， 状态码为:{}'.format(response.status_code))
                # self.get_str(self, url, headers=self.headers, encoding=encoding)

class TestDownload:
    """阿布云测试"""
    def __init__(self, logger):
        # ua = UserAgent().random
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        self.headers = {
            'User-Agent': self.ua,
            'Connection': 'close'
        }
        self.logger = logger

    def get_str(self, url, headers={}, encoding='utf-8'):
        if headers:
            self.headers.update(headers)
        self.headers["User-Agent"] = self.ua
        try:
            proxyurl = config.ABY_URI_TEST
            response = requests.get(url, headers=self.headers,
                                    timeout=30, verify=False)

        except ProxyError:
            self.logger.info("代理异常...")
        except Exception as e:
            self.logger.info('其它错误：' + str(e))
            time.sleep(random.randint(1, 15)/10)
        else:
            print(response.status_code)
            print("请求:", url)
            print("返回", response.url)
            if response.status_code == 404:
                result = {'str': '404', 'link': response.url}
                return result
            elif response.status_code == 200:
                html_str = response.content.decode(encoding, 'ignore')
                result = {'str': html_str, 'link': response.url}
                return result
            else:
                self.logger.info('下载错误， 状态码为:{}'.format(response.status_code))
                # self. get_str(self, url, headers={}, encoding='utf-8')


class FangDownload:
    """代理云"""

    def __init__(self, logger):
        # ua = UserAgent().random
        ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        self.headers = {
            'User-Agent': ua,
        }
        self.logger = logger

    def get_str(self, url, headers={}):
        if headers:
            self.headers.update(headers)

        try:
            while True:
                proxyurl = common_dlyproxy.get_proxy(self.logger)
                if proxyurl:
                    break
            self.logger.info('the proxy is :'+proxyurl)

            response = requests.get(url, headers=self.headers, timeout=30, proxies={'http':proxyurl,'https':proxyurl}, verify=False)
        except ConnectTimeout as e:
            self.logger.info('get_str---' + str(e))
            self.get_str(url)
        except TimeoutError as e:
            self.logger.info('get_str---'+str(e))
            self.get_str(url)

        except Exception as e:
            self.logger.info('1---'+str(e))
            self.get_str(url)

        else:
            print(url)
            print(response.url)
            if response.close().status_code == 404:
                result = {'str': '404', 'link': response.url}
                return result
            elif response.status_code == 200 and response.url.strip(
                    "htps").replace("esf1", "esf") == url.strip("htps").replace("esf1", "esf"):

                html_str = response.content.decode('utf-8', 'ignore')
                result = {'str': html_str, 'link': response.url}
                return result
            else:
                result = {'str': "", 'link': response.url}
                return result


if __name__ == '__main__':
    pass

