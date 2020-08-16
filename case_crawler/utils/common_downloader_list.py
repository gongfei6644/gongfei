# condeing=utf-8
import datetime
import random

import requests
# import redis
# import Proxies
from lxml import etree
import traceback
import time
import json
import urllib3
from requests.exceptions import ProxyError
from selenium import webdriver

from setting import config
from utils.common_tools import ClsSingleton
from utils.constants import RETRY_TIMES_MAP

urllib3.disable_warnings()


class crawling(ClsSingleton):
    """
    下载器
    """
    proxyurl = config.ABY_URI_LIST

    def __init__(self, source=None, logger=None):
        self.source = source
        self.logger = logger
        self.proxy = config.ABY_URI_MAP.get(source, config.ABY_URI_LIST)
        self.headers = {'User-Agent': random.choice(config.AGENT_LIST)}
        self.driver = None

    def get(self, url, headers, encoding="utf-8"):
        '''
         get 方式获取页面数据
        :param check_element: 爬取页面需检查的元素
        :param url: 爬取的url ，为空则默认类中的url
        :param headers: 请求头，为空则默认类中的 headers
        :param encoding: 页面编码，默认utf-8
        :return: 返回 requests.text
        '''
        self.headers = {'User-Agent': random.choice(config.AGENT_LIST)}
        if headers:
            self.headers.update(headers)
        try:
            proxies = {'http': self.proxyurl, 'https': self.proxyurl}
            response = requests.get(url, headers=self.headers, proxies=proxies, timeout=30, verify=False)
            content = response.content.decode(encoding, "ignore")
            url = response.url
            if response.url.strip("https") != url.strip("https"):
                content = "verify"
                self.logger.info("重定向:{}, to:{}".format(url, response.url))
            elif response.status_code == 404 or not url.startswith("http"):
                content = "404"
        except Exception as ex:
            content = "verify"
            self.logger.error("crawling get 函数 爬取页面出错:{};错误信息：{};{}".format(
                url, ex, traceback.extract_stack()))
        finally:

            return content

    def post(self, url="", headers=None, json_data=""):
        '''
        :param json_data: js数据格式
        :param check_element: 检查爬取的页面元素
        :param url:
        :param headers:
        :param encoding:
        :return:
        '''
        self.headers = {'User-Agent': random.choice(config.AGENT_LIST)}
        if headers:
            self.headers.update(headers)

            for i in range(RETRY_TIMES_MAP[self.source]):
                try:
                    response = requests.post(url, headers=self.headers, data=json_data, proxies={
                    "http": self.proxy, "https": self.proxy}, timeout=30, verify=False)
                    self.logger.info("第{}次重试,code:{}".format(i, response.status_code))
                    if response.status_code == 200 and url.lstrip('https') == response.url.lstrip("https"):
                        content = response.content.decode("utf-8", "ignore")
                        return content
                    elif response.status_code == 404 or "404" in response.url:
                        content = "404"
                        return content
                    else:
                        time.sleep(0.1)
                except ProxyError:
                    # 未获取到隧道资源,返回重试标识
                    content = "retry"
                    self.logger.info("第{}次重试出现代理异常".format(i))
                except Exception as ex:
                    msg = "第{}次post请求异常, {}".format(i, ex)
                    self.logger.error(msg)
            else:
                time.sleep(random.randint(10, 100)/10)
                self.logger.error("连续{}次post请求失败{}".format(RETRY_TIMES_MAP[self.source], url))

    def get_by_abucloud(self, url, headers=None, encoding="utf-8"):
        '''
        :param url: 爬取的url ，为空则默认类中的url
        :param headers: 请求头，为空则默认类中的 headers
        :param encoding: 页面编码，默认utf-8
        :return: content 有3种状态: 正常网页数据的str / "404" / "retry"
        '''
        self.logger.info("进入下载:{}".format(url))
        self.headers = {'User-Agent': random.choice(config.AGENT_LIST)}
        if headers:
            self.headers.update(headers)
        content = ""
        for i in range(RETRY_TIMES_MAP[self.source]):
            try:
                response = requests.get(url, headers=self.headers, proxies={
                    "http": self.proxy, "https": self.proxy}, timeout=30, verify=False)
                self.logger.info("第{}次重试,code:{}".format(i, response.status_code))
                self.logger.info("\n访问链接 {}\n返回链接 {}".format(url, response.url))
                if response.status_code == 200 and response.url.replace("esf1", "esf") == url.replace("esf1", "esf"):
                    content = response.content.decode(encoding, "ignore")
                    break
                elif response.status_code == 404 or "/404." in response.url:
                    content = "404"
                    break
                else:
                    content = "retry"
                    # self.logger.info("{}进入retry, code:{}".format(url, response.status_code))
            except ProxyError as e:
                # 未获取到隧道资源,返回重试标识
                content = "retry"
                self.logger.info("第{}次重试,代理异常: {}".format(i, e))
            except Exception as ex:
                content = "retry"
                self.logger.error("第{}次重试,出现异常,错误信息：{}".format(i, ex))
        else:
            self.logger.info("连续{}次请求失败{}".format(RETRY_TIMES_MAP[self.source], url))
        time.sleep(0.5)
        return content

    def get_by_chrome(self, url):
        """使用chrome渲染"""
        self.logger.info("进入下载:{}".format(url))
        content = ""
        try:
            if not self.driver:
                self.driver = webdriver.Chrome()
            self.driver.get(url)
            self.driver.refresh()
            time.sleep(random.randint(3, 10))
            first = self.driver.find_element_by_xpath('//h4[1]/a')
            first.click()
            self.driver.switch_to.window(self.driver.window_handles[-1])

            print(1111111111)
            time.sleep(5)
            ref = self.driver.get_log('client')
            self.driver.refresh()
            input()
            print(22222222222222)
            content = self.driver.page_source
        except Exception as e:
            content = "retry"
            self.logger.error("{}下载异常{}".format(url, e))
            self.driver.quit()
        finally:
            return content


    def check_func(self, content, check_element):
        '''
         检查节点是否存在
        :param content:  爬取页面内容
        :param check_element: 检查的页面元素
        :return:
        '''
        try:
            if content is None:
                return False
                root = etree.HTML(content)
            items = root.xpath(check_element)
            if items:
                return True
            else:
                return False
        except Exception  as error:
            return False


    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass
