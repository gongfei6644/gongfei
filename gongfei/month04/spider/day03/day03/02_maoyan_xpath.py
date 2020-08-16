import requests
from lxml import etree
import time
import random

class MaoyanSpider(object):
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        self.headers = {
            'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
        }
        # 添加计数变量
        self.page = 1

    def get_page(self,url):
        res = requests.get(
            url,
            headers=self.headers
        )
        res.encoding = 'utf-8'
        html = res.text
        # 直接调用解析函数
        self.parse_page(html)

    # 用xpath数据提取
    def parse_page(self,html):
        # 创建解析对象
        parse_html = etree.HTML(html)
        # 基准xpath,获取dd节点对象列表
        dd_list = parse_html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
        # for遍历,依次获取每个电影dd信息
        for dd in dd_list:
            # 名称
            name = dd.xpath('./div/div/div[1]/p[1]/a/text()')
            if name:
                name = name[0].strip()
            else:
                name = 'null'

            # 主演
            star = dd.xpath('./div/div/div[1]/p[2]/text()')
            if star:
                star = star[0].strip()
            else:
                star = 'null'

            # 时间
            time = dd.xpath('./div/div/div[1]/p[3]/text()')
            if time:
                time = time[0].strip()[5:15]
            else:
                time = 'null'

            print(
                {
                    '名称' : name,
                    '主演' : star,
                    '时间' : time
                }
            )



    def main(self):
        for offset in range(0,21,10):
            url = self.url.format(str(offset))

            self.get_page(url)
            print('第%d页完成' % self.page)
            self.page += 1
            time.sleep(random.randint(1,3))

if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.main()















