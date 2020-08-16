from urllib import request
import re
import time
import random

class FilmSkySpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'
        }

    # 获取响应内容(两级页面)
    def get_page(self,url):
        req = request.Request(
            url,
            headers=self.headers
        )
        res = request.urlopen(req)
        # decode()第二个参数,ignore,忽略掉解码异常
        html = res.read().decode('gb2312','ignore')

        return html

    # 解析一级页面
    def parse_one_page(self,html):
        pattern = re.compile('<table width="100%".*?<a href="(.*?)".*?>(.*?)</a>',re.S)
        film_list = pattern.findall(html)
        # film_list: [('/html/xxx','这个男人'),()]
        for film in film_list:
            # 电影名称
            name = film[1].strip()
            # 电影链接
            link = 'https://www.dytt8.net' + film[0].strip()
            # 向link发请求,获取下载链接(二级页面)
            download_link = self.get_two_page(link)

            print([name,download_link])

    # 解析二级页面
    def get_two_page(self,link):
        # 发请求
        html = self.get_page(link)
        # 解析
        pattern = re.compile('<td style="WORD-WRAP.*?<a href="(.*?)"',re.S)

        return pattern.findall(html)[0]


if __name__ == '__main__':
    url = 'https://www.dytt8.net/html/gndy/dyzz/index.html'
    spider = FilmSkySpider()
    html = spider.get_page(url)
    spider.parse_one_page(html)













