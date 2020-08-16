
import time
import random
import requests
# from fake_useragent import UserAgent
from lxml import etree
from requests.exceptions import ProxyError,Timeout
from threading import Lock

from setting import config
from requests import ConnectTimeout
from utils import common_dlyproxy
from utils.common_redis import conn
from utils.common_tools import get_proxy_ip

lock = Lock()

class Downloader:
    """阿布云"""
    def __init__(self, logger=None, source="other"):
        self.source = source
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        self.logger = logger

    def get_str(self, url, headers=None, encoding='utf-8'):

        if headers:
            self.headers.update(headers)
        self.headers["User-Agent"] = random.choice(config.AGENT_LIST)

        try:
            # time.sleep(random.randint(1,1000)/1000)
            if self.source == "安居客租房" or self.source == '58同城租房':
                random_num = random.randint(1, 5)
                if random_num > 2:
                    response = requests.get(
                        url, headers=self.headers, proxies={
                            'http': config.ABY_URI, 'https': config.ABY_URI},timeout=30, verify=False)
                else:
                    proxy = get_proxy_ip(self.source)
                    valid_time = conn.ttl(proxy)
                    value = conn.get(proxy)
                    response = requests.get(
                        url, headers=self.headers, proxies={
                            'http': proxy, 'https': proxy}, timeout=30, verify=False)
            else:
                proxy = get_proxy_ip(self.source)
                valid_time = conn.ttl(proxy)
                value = conn.get(proxy)
                response = requests.get(
                    url, headers=self.headers, proxies={
                        'http': proxy, 'https': proxy}, timeout=30, verify=False)
        except ProxyError:
            self.logger.info('代理异常...')
            if self.source != "安居客租房" and self.source != '58同城租房':
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
            if self.source != "安居客租房" and self.source != '58同城租房':
                try:
                    conn.set(proxy, self.source + value, ex=valid_time)
                except:
                    pass
            elif (self.source == '安居客租房' or self.source == '58同城租房') and random_num == 1:
                try:
                    conn.set(proxy, self.source + value, ex=valid_time)
                except:
                    pass
        except Exception as e:
            self.logger.info('其它错误：' + str(e))
        else:
            if response.status_code == 404:
                result = {'str': '404', 'link': response.url}
                html_str = response.content.decode(encoding, 'ignore')
                if self.source == "房天下租房":
                    nonexistent_str = "很抱歉，您访问的页面可能已经删除或不可用，建议您访问其他页面！"
                    if nonexistent_str in html_str:
                        result = {'str': '访问页面不存在', 'link': response.url}
                elif self.source == "安居客租房":
                    nonexistent_str = "对不起，您要浏览的网页可能被删除，重命名或者暂时不可用"
                    nonexistent_str_1 = '抱歉,您要查看的页面丢失了'
                    if nonexistent_str in html_str or nonexistent_str_1 in html_str:
                        result = {'str': '访问页面不存在', 'link': response.url}
                return result
            elif response.status_code == 200:
                if self.source == "房天下租房":
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
                                cookie = "global_cookie=nwv5jgfpbkuckdkwa0nxt3a2k17jztez4ee; __utmc=147393320; keyWord_recenthousezhoukou=%5b%7b%22name%22%3a%22%e5%85%b3%e5%b8%9d%e5%ba%99%22%2c%22detailName%22%3a%22%e5%b7%9d%e6%b1%87%e5%8c%ba%22%2c%22url%22%3a%22%2fhouse-a011791-b015829%2fh31%2f%22%2c%22sort%22%3a2%7d%5d; keyWord_recenthousexinyang=%5b%7b%22name%22%3a%22%e5%8c%97%e4%ba%ac%e8%b7%af%22%2c%22detailName%22%3a%22%e6%b5%89%e6%b2%b3%e5%8c%ba%22%2c%22url%22%3a%22%2fhouse-a011781-b015125%2fh31%2f%22%2c%22sort%22%3a2%7d%5d; ASP.NET_SessionId=tsysyiwdrx2unwdq3ru0ayhw; Rent_StatLog=a61623df-1ab7-45cd-b468-29af58e688b8; keyWord_recenthousekaifeng=%5b%7b%22name%22%3a%22%e9%bc%93%e6%a5%bc%22%2c%22detailName%22%3a%22%e9%bc%93%e6%a5%bc%22%2c%22url%22%3a%22%2fhouse-a011354-b013095%2fh31-i33%2f%22%2c%22sort%22%3a2%7d%5d; city=xinyang; __utmz=147393320.1571292365.11.10.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-80ae9b14ce940b3d2b/redirect; Captcha=6E73434F354C70397478524134526C594C3264662B4C636165676332495A4C766F4A3143314C4A6A6F78737A433737565A776E61482B7358354C424C4168712F4E4245344355644A5A49553D; g_sourcepage=zf_fy%5Egrxq_pc; unique_cookie=U_sc5spjnso1dhj4dw5hhx40r0526k1sloqsc*25; __utma=147393320.1531583592.1566885175.1571292365.1571303623.12; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.3.10.1571303623"
                                headers = {
                                    "cache-control": "no-cache",
                                    "referer": referer,
                                    "cookie": cookie,
                                    'User-Agent': random.choice(config.AGENT_LIST)
                                }
                                response_next = requests.get(href, headers=headers, proxies={
                                    "http": proxy, "https": proxy}, timeout=30, verify=False)
                                if response_next.status_code == 200:
                                    html_str = response_next.content.decode(encoding, "ignore")
                                    result = {'str': html_str, 'link': response_next.url}
                                    return result
                            except ProxyError:
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
                                self.logger.error("房天下重定向第{}次重试,出现异常,错误信息：{}".format(i, ex))
                    else:
                        # print(response.url)
                        # print(result.decode('gbk','ignore'))
                        return
                html_str = response.content.decode(encoding, 'ignore')
                result = {'str': html_str, 'link': response.url}
                if self.source == "58同城租房":
                    nonexistent_str = "该页面可能被删除、转移或暂时不可用"
                    if nonexistent_str in html_str:
                        result = {'str': '访问页面不存在', 'link': response.url}
                return result
            else:
                self.logger.info('下载错误， 状态码为:{}'.format(response.status_code))
                print("下载失败异常码", response.status_code, '请求链接：',url,'返回链接：',response.url)




class DailiyunDownload:
    """代理云"""

    def __init__(self, logger):
        # ua = UserAgent().random
        ua = "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1"
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

            response = requests.get(url, headers=self.headers, timeout=20, proxies={'http':proxyurl,'https':proxyurl}, verify=False)
        except ProxyError:
            pass
        except Exception as e:
            self.logger.info('1---'+str(e))
            self.get_str(url)
            result = {'str': "", 'link': url}
            return result

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

