# condeing=utf-8
import datetime
import random
import re

import requests
# import redis
# import Proxies
from lxml import etree
import traceback
import time
import json
import urllib3
from requests.exceptions import ProxyError,ConnectTimeout
from requests.exceptions import Timeout
from selenium import webdriver
from threading import Lock


from setting import config
from utils.common_redis import conn
from utils.common_tools import ClsSingleton, get_proxy_ip
from utils.constants import RETRY_TIMES_MAP

urllib3.disable_warnings()

lock = Lock()

class crawling(ClsSingleton):
    """
    下载器
    """
    proxyurl = config.ABY_URI

    def __init__(self, source=None, logger=None):
        self.source = source
        self.logger = logger
        self.proxy = config.ABY_URI
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
            if self.source == '安居客租房' or self.source == '58同城租房':
                proxies = {'http': self.proxyurl, 'https': self.proxyurl}
            else:
                proxy = get_proxy_ip(self.source)
                valid_time = conn.ttl(proxy)
                value = conn.get(proxy)
                proxies = {'http': proxy, 'https': proxy}
            response = requests.get(url, headers=self.headers, proxies=proxies, timeout=30, verify=False)
            content = response.content.decode(encoding, "ignore")
            url = response.url
            if response.url.strip("https") != url.strip("https"):
                content = "verify"
                self.logger.info("重定向:{}, to:{}".format(url, response.url))
            elif response.status_code == 404 or not url.startswith("http"):
                content = "404"
        except ProxyError:
            self.logger.info('代理异常...')
            if self.source != '安居客租房' and self.source != '58同城租房':
                try:
                    conn.set(proxy, self.source + value, ex=valid_time)
                except:
                    pass
        except Timeout as e:
            self.logger.info('连接超时：' + str(e))
            if self.source != '安居客租房' and self.source != '58同城租房':
                try:
                    conn.set(proxy, self.source + value, ex=valid_time)
                except:
                    pass
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
                    if self.source == '安居客租房' or self.source == '58同城租房':
                        response = requests.post(url, headers=self.headers, data=json_data, proxies={
                        "http": self.proxy, "https": self.proxy}, timeout=30, verify=False)
                    else:
                        proxy = get_proxy_ip(self.source)
                        valid_time = conn.ttl(proxy)
                        value = conn.get(proxy)
                        response = requests.post(url, headers=self.headers, data=json_data, proxies={
                            "http": proxy, "https": proxy}, timeout=30, verify=False)
                        if self.source == "城市房产租房":
                            returnCitySN_url = 'https://pv.sohu.com/cityjson?ie=utf-8'
                            try:
                                returnCitySN_ = requests.get(returnCitySN_url, proxies={
                                "http": proxy, "https": proxy}, timeout=10, verify=False)
                                if returnCitySN_:
                                    returnCitySN = returnCitySN_.text
                                    # print(returnCitySN)
                                else:
                                    continue
                            except ProxyError:
                                continue
                            except Timeout as e:
                                continue
                            except Exception as e:
                                continue

                    self.logger.info("第{}次post请求重试,code:{}".format(i, response.status_code))
                    self.logger.info("\n访问链接 {}\n返回链接 {}".format(url, response.url))
                    if response.status_code == 200 and url.lstrip('https') == response.url.lstrip("https"):
                        content = response.content.decode("utf-8", "ignore")
                        if self.source == "城市房产租房":
                            content = (content, returnCitySN)
                        return content
                    else:
                        time.sleep(0.1)
                except Timeout as e:
                    self.logger.info('连接超时：' + str(e))
                    if self.source != '安居客租房' and self.source != '58同城租房':
                        try:
                            conn.set(proxy, self.source + value, ex=valid_time)
                        except:
                            pass
                except ProxyError:
                    # 未获取到隧道资源,返回重试标识
                    content = "retry"
                    self.logger.info("第{}次重试出现代理异常".format(i))
                    if self.source != '安居客租房' and self.source != '58同城租房':
                        try:
                            conn.set(proxy, self.source + value, ex=valid_time)
                        except:
                            pass
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
                time.sleep(random.randint(1,500)/500)
                if self.source == '安居客租房' or self.source == '58同城租房':
                    random_num = random.randint(1, 5)
                    if random_num > 2:
                        response = requests.get(url, headers=self.headers, proxies={
                            "http": self.proxy, "https": self.proxy}, timeout=30, verify=False)
                    else:
                        proxy = get_proxy_ip(self.source)
                        valid_time = conn.ttl(proxy)
                        value = conn.get(proxy)
                        response = requests.get(url, headers=self.headers, proxies={
                            "http": proxy, "https": proxy}, timeout=30, verify=False)
                else:
                    proxy = get_proxy_ip(self.source)
                    valid_time = conn.ttl(proxy)
                    value = conn.get(proxy)
                    response = requests.get(url, headers=self.headers, proxies={
                        "http": proxy, "https": proxy}, timeout=30, verify=False)
                    # print(response.text)
                self.logger.info("第{}次重试,code:{}".format(i, response.status_code))
                self.logger.info("\n访问链接 {}\n返回链接 {} code:{}".format(url, response.url,response.status_code))
                if self.source == "房天下租房" and response.status_code == 200:
                    result = response.content.decode('utf-8', "ignore")
                    html = etree.HTML(result)
                    href = html.xpath('string(//a[contains(./text(),"点击跳转")]/@href)')
                    if href:
                        for i in range(50):
                            proxy = get_proxy_ip(self.source)
                            valid_time = conn.ttl(proxy)
                            value = conn.get(proxy)
                            try:
                                referer = url
                                cookie = "global_cookie=858rxappvbibay2xvvj0knhnj2zjpdnfwnn; Integrateactivity=notincludemc; lastscanpage=0; newhouse_user_guid=8F79FB4C-E7E7-A82F-1EAB-80A740138AA1; searchConN=1_1562072520_529%5B%3A%7C%40%7C%3A%5Db2755e4c34cf6f19bdf36bf7f5e7f252; vh_newhouse=1_1562135369_1723%5B%3A%7C%40%7C%3A%5Dc986ba3e7921e9c51a1d863325527852; new_search_uid=6beab057a77eed00b3111dba591ed79b; integratecover=1; __utmc=147393320; newhouse_chat_guid=F338123B-36B6-B946-6D33-B9BEDD74088F; keyWord_recenthouseaba=%5b%7b%22name%22%3a%22%e5%a3%a4%e5%a1%98%e5%8e%bf%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a013524%2f%22%2c%22sort%22%3a1%7d%5d; keyWord_recenthouseakesu=%5b%7b%22name%22%3a%22%e9%98%bf%e5%85%8b%e8%8b%8f%e5%b8%82%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a013308%2f%22%2c%22sort%22%3a1%7d%5d; keyWord_recenthousezz=%5b%7b%22name%22%3a%22%e9%87%91%e6%b0%b4%e5%8c%ba%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a0362%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e5%af%8c%e7%94%b0%e5%a4%a7%e5%8e%a6%22%2c%22detailName%22%3a%22%e9%87%91%e6%b0%b4%e5%8c%ba%22%2c%22url%22%3a%22%2fhouse-a0362-b04543%2f%22%2c%22sort%22%3a2%7d%5d; keyWord_recenthousesh=%5b%7b%22name%22%3a%22%e9%9d%99%e5%ae%89%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a021%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e5%8d%97%e4%ba%ac%e8%a5%bf%e8%b7%af%22%2c%22detailName%22%3a%22%e9%9d%99%e5%ae%89%22%2c%22url%22%3a%22%2fhouse-a021-b01623%2f%22%2c%22sort%22%3a2%7d%5d; Rent_StatLog=dac051f3-2f97-4739-b401-dc504f65fc21; keyWord_recenthousebj=%5b%7b%22name%22%3a%22%e6%9c%9d%e9%98%b3%22%2c%22detailName%22%3a%22%22%2c%22url%22%3a%22%2fhouse-a01%2fh350%2f%22%2c%22sort%22%3a1%7d%2c%7b%22name%22%3a%22%e5%a5%a5%e6%9e%97%e5%8c%b9%e5%85%8b%e5%85%ac%e5%9b%ad%22%2c%22detailName%22%3a%22%e6%9c%9d%e9%98%b3%22%2c%22url%22%3a%22%2fhouse-a01-b02652%2fh350%2f%22%2c%22sort%22%3a2%7d%2c%7b%22name%22%3a%22CBD%22%2c%22detailName%22%3a%22%e6%9c%9d%e9%98%b3%22%2c%22url%22%3a%22%2fhouse-a01-b05510%2fh31-i350%2f%22%2c%22sort%22%3a2%7d%5d; keyWord_recenthousely=%5b%7b%22name%22%3a%22%e9%ab%98%e6%96%b0%22%2c%22detailName%22%3a%22%e6%b6%a7%e8%a5%bf%e5%8c%ba%22%2c%22url%22%3a%22%2fhouse-a010204-b012374%2fh31%2f%22%2c%22sort%22%3a2%7d%5d; __utma=147393320.1504671198.1563161384.1564038187.1564103717.15; __utmz=147393320.1564103717.15.11.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/redirect; city=ly; g_sourcepage=zf_fy%5Elb_pc; ASP.NET_SessionId=3lxrim4ydfq2welakqlme3rx; unique_cookie=U_h9ltwhyjfb0i30sq7dacdbqov1pjye39uzw*147; Captcha=667370653855576D5055674779706535414B783149554A6744382F3348333448505266706659466137332F417557444E484F367A71474B5546484D394A345545326E313050664D544548673D; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.9.10.1564103717"
                                headers = {
                                    "cache-control": "no-cache",
                                    "referer": referer,
                                    "cookie": cookie,
                                    'User-Agent': random.choice(config.AGENT_LIST)
                                }
                                response_next = requests.get(href, headers=headers, proxies={
                                    "http": proxy, "https": proxy}, timeout=30, verify=False)
                                if response_next.status_code == 200:
                                    content = response_next.content.decode(encoding, "ignore")
                                    return content
                            except ProxyError:
                                content = "retry"
                                self.logger.info("房天下重定向第{}次重试,代理异常...".format(i))
                                try:
                                    conn.set(proxy, self.source + value, ex=valid_time)
                                except:
                                    pass
                            except Timeout as e:
                                self.logger.info('连接超时：' + str(e))
                                try:
                                    conn.set(proxy, self.source + value, ex=valid_time)
                                except:
                                    pass
                            except Exception as ex:
                                content = "retry"
                                self.logger.error("房天下重定向第{}次重试,出现异常,错误信息：{}".format(i, ex))
                    else:
                        return
                elif response.status_code == 200 and response.url.replace("esf1", "esf") == url.replace("esf1", "esf"):
                    content = response.content.decode(encoding, "ignore")
                    break
                elif response.status_code == 404 or "/404." in response.url:
                    content = "404"
                    break
                else:
                    content = "retry"
                    # self.logger.info("{}进入retry, code:{}".format(url, response.status_code))
            except ProxyError:
                # 未获取到隧道资源,返回重试标识
                content = "retry"
                self.logger.info("第{}次重试,代理异常...".format(i))
                if self.source != '安居客租房' and self.source != '58同城租房':
                    try:
                        conn.set(proxy, self.source + value, ex=valid_time)
                    except:
                        pass
                elif (self.source == '安居客租房' or self.source == '58同城租房') and random_num == 1:
                    try:
                        conn.set(proxy, self.source + value, ex=valid_time)
                    except:
                        pass
            except Timeout as e:
                self.logger.info('连接超时：' + str(e))
                if self.source != '安居客租房' and self.source != '58同城租房':
                    try:
                        conn.set(proxy, self.source + value, ex=valid_time)
                    except:
                        pass
                elif (self.source == '安居客租房' or self.source == '58同城租房') and random_num == 1:
                    try:
                        conn.set(proxy, self.source + value, ex=valid_time)
                    except:
                        pass
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
            # if not self.driver:
            proxy = get_proxy_ip(self.source)
            chromeOptions = webdriver.ChromeOptions()
            # 设置不加载图片
            prefs = {"profile.managed_default_content_settings.images": 2}
            chromeOptions.add_experimental_option("prefs", prefs)
            # 设置无头
            chromeOptions.add_argument('--headless')
            chromeOptions.add_argument('--disable-gpu')
            user_agent = random.choice(config.AGENT_LIST)
            if user_agent:
                chromeOptions.add_argument('user-agent=' + user_agent)

            # 设置代理
            chromeOptions.add_argument("--proxy-server=%s" % proxy)
            self.driver = webdriver.Chrome(chrome_options=chromeOptions)

            self.driver.get(url)
            # 给留出时间加载网页新的商品
            time.sleep(random.randint(20, 30) / 10)

            time.sleep(random.randint(10, 30)/10)
            content = self.driver.page_source
        except Exception as e:
            content = "retry"
            self.logger.error("{}下载异常{}".format(url, e))
            self.driver.quit()
        finally:
            self.driver.quit()
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



